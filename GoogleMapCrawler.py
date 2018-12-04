from selenium import webdriver
import time
import _thread
import datetime

# prevent loading image and set up disk cache
#chromeOptions = webdriver.ChromeOptions()
#prefs = { 'disk-cache-size':4096}
#chromeOptions.add_experimental_option('prefs', prefs)



# The search start point is HKU
startPoint = "@22.2860628,114.1292237,15z"
InitialURL = "https://www.google.com.hk/maps"
TargetURL = InitialURL + "/" + startPoint + "?hl=en"


timeDelay = 5
timeMiniDelay = 0.2
nullValue = "None"
maxAttempt = 20 # maxmimum attempt to locate element

propertyURL_buy = "https://www.28hse.com/en/buy"
propertyURL_rent = "https://www.28hse.com/en/rent"

set_keywords = ["school","hospital","bank","restaurant","bar","coffee","parking lot","post office", "supermarket", "park", "garden", "beach", "store","bus terminal","sport center","University","McDonald","Theater","Mall","FireStation","Police office","ATM","Gas station","Temple"]
start_index = 3
current_key_word = ""

main_driver = webdriver.Chrome()
main_driver.get(TargetURL)
main_driver.implicitly_wait(timeDelay)

translation_driver = webdriver.Chrome()
translation_driver.get(TargetURL)
translation_driver.implicitly_wait(timeDelay)

# file to write
fileName = str(time.ctime()) + ".txt"
fileName = fileName.replace(":", "-")
outputFile = open(fileName,"a", encoding='utf-8')
def appendToFile(content):
	outputFile.write(content)



def go_back(driver):
	#back_button = driver.find_element_by_xpath("//button[@class='section-back-to-list-button blue-link noprint']")
	back_button = find_element_by_xpath_until_found(driver, "//button[@class='section-back-to-list-button blue-link noprint']", False)
	back_button.click()

#time.sleep(5)
def init_search(driver, keyword):	
	#SearchBarInput = driver.find_element_by_xpath("//input[@id='searchboxinput']")
	#SearchBarInput = driver.find_element_by_xpath("input[@class='tactile-searchbox-input']")
	SearchBarInput = find_element_by_xpath_until_found(driver, "//input[@id='searchboxinput']", False)
	SearchBarInput.click()
	SearchBarInput.clear()
	SearchBarInput.send_keys(keyword)

	#SearchBarButton = driver.find_element_by_xpath("//button[@id='searchbox-searchbutton']")
	SearchBarButton = find_element_by_xpath_until_found(driver, "//button[@id='searchbox-searchbutton']", False)
	SearchBarButton.click()

def get_result_div(driver):
	result_div_list = driver.find_elements_by_class_name("section-result")
	#print("div list: ", result_div_list)
	while len(result_div_list) == 0:# if not found, meaning that is not loaded yet
		#time.sleep(timeMiniDelay)
		result_div_list = driver.find_elements_by_class_name("section-result")
	for count in range(0, len(result_div_list)):
		current_div_list = driver.find_elements_by_class_name("section-result")
		while len(current_div_list) == 0:
			current_div_list = driver.find_elements_by_class_name("section-result")
		fetch_return(main_driver, current_div_list[count])

def fetch_return(driver, div):
	div.click()
	#time.sleep(5)
	#location_name = driver.find_elements_by_class_name("section-hero-header-description").text
	#location_name = driver.find_element_by_xpath("//div[@class='section-hero-header-description']//h1[@class='section-hero-header-title']").text
	location_name = find_element_by_xpath_until_found(driver, "//div[@class='section-hero-header-description']//h1[@class='section-hero-header-title']", True)
	#rating = driver.find_elements_by_class_name("//div[@class='section-hero-header-description']/div[@class='section-hero-header-description-container']/div/div/span/span/span").text
	all_info = driver.find_elements_by_class_name("widget-pane-link")
	
	text = [info.text for info in all_info if len(info.text) > 0]
	print("text length:",len(text), "\n")
	#index_adjust = max(len(text) - 8, 0)
	plus_code_location = "11AA+A1"
	for t in text:
		splited = t.split(' ')
		if len(splited) != 3:
			continue
		if splited[1] == "Hong" and splited[2] == "Kong":
			plus_code_location = t
	#check if has review
	if text[0].find("review") == -1:
		#index_adjust -= 1
		store_info(location_name,0,0,text[0],text[1], plus_code_location)
	else:
		store_info(location_name, 0, text[0], text[1], text[2], plus_code_location)
	current_url = driver.current_url
	#driver.back()
	go_back(driver)
	while driver.current_url == current_url:
		time.sleep(timeMiniDelay)
		print("going back")



def store_info(place_name, rating, review_num, keyword, addr, location):
	info = "".join(["place name: ", place_name,"\n",
		  		"rating", "no rating currently","\n",
		  		"review_num", str(review_num),"\n",
		  		"keyword: ", keyword, "\n",
		  		" address: ", addr, "\n",
		  		" Location: ", location, "\n"])
	#print(info.encode('utf-8'))
	info_to_store = place_name + "@" + str(review_num).split(' ')[0] + "@" + current_key_word + "@" + keyword + "@" + addr + "@" + translate_plusCode(location) + "\n"
	appendToFile(info_to_store)
	#_thread.start_new_thread(thread_store_info_to_file,(info_to_store, location))


def thread_store_info_to_file(info, location_plusCode):
	coordinate = translate_plusCode(location_plusCode)
	result = info+"@"+coordinate
	appendToFile(result)

def turn_page(driver):
	try:
		next_button = driver.find_element_by_xpath("//span[@class='section-pagination-button-next']")
		next_button.click()
		#element_index = driver.find_element_by_class_name("section-pagination-right")
		#page_info = element_index.text
		#info_list = page_info.split(' ')
		#print(element_index.text)
	except:
		# can not click, no next page
		return False
	return True
	#time.sleep()


def translate_plusCode(plus_code):
	init_search(translation_driver, plus_code)
	while True:
		try:
			#coordinate_text = translation_driver.find_element_by_xpath("//div[@class='section-hero-header-description']//h2[@class='section-hero-header-subtitle']").text
			coordinate_text = find_element_by_xpath_until_found(translation_driver, "//div[@class='section-hero-header-description']//h2[@class='section-hero-header-subtitle']", True)
			#print(coordinate_span.text)
			return coordinate_text
		except:
			time.sleep(timeMiniDelay)
			print("translation_driver stucked")



def find_element_by_xpath_until_found(driver, xpath, isText):
	count = 0
	while True:
		try:
			element = driver.find_element_by_xpath(xpath)
			if isText:
				return element.text
			else:
				return element
		except:
			count += 1
			print("locating element stuck when finding", xpath, " with count ", count)
			if count >= maxAttempt and isText:
				return nullValue
			time.sleep(timeMiniDelay)
			pass




def start(driver):
	for k in range(start_index,len(set_keywords)):
		current_key_word = set_keywords[k]
		init_search(driver, current_key_word)
		while True:
			time.sleep(timeDelay)
			get_result_div(driver)
			if turn_page(driver) == False:
				break

start(main_driver)
#turn_page(main_driver)
#translate_plusCode("74PP+2V Hong Kong")
