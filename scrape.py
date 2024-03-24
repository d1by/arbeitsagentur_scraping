##########################
# Default values (for tests): 
search_term = "Computer Science"
num_of_res = 30
##########################
# modify based on network capabilities
# (for slower internet connections, use a higher wait time)
wait_time = 3 # e.g. 3 -> 30 seconds
##########################


from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re
import csv
import sys

options = FirefoxOptions()

# TO DO: allow user to choose between gui and headless modes
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(30)

# driver.get("https://google.com/")
# print("Google opened. ")

res_count = 0

def main():
    driver.get("https://www.arbeitsagentur.de/kursnet")
    print(f"opened {driver.current_url}")

    # cookie popup
    # MAYBE: put inside a function, call again on 'opportunities' page
    cookie_btn_path = '//*[@id="bahf-cookie-disclaimer-modal"]/div/div/div[3]/button[1]/bahf-i18n'
    
    for i in range(10):
        try:
            if elem := WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cookie_btn_path))):
                print("Located cookie popup. ")
                
                elem.click()
                print("Closed cookie popup. ")

                break
        except:
            print(f"Failed to locate cookie popup ({i+1}/10).")
            if(i%2==0):
                print("Refreshing...")
                driver.refresh()
            pass


    #driver.find_element(By.XPATH, cookie_btn_path).click()

    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable('//*[@id="bahf-cookie-disclaimer-modal"]')).click()

    opp_path = f'//*[@id="main"]/div[1]/section/div[1]/section/a'

    # TO DO: waiting for overlays to become invisible is very very slow
    # removing this and using try/except breaks the code
    # analyze later and find a better way

    print("Locating overlays... ")

    _ = WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "bahf-cookie-disclaimer-modal"))
    )

    print("First overlay closed. ")

    _ = WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "bahf-cookie-disclaimer-dp13"))
    )

    print("Second overlay closed. ")

    #driver.find_element(By.XPATH, opp_path).click()

    for _ in range(10):
        try:
            if elem := WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, opp_path))):
                print("Located opportunities page. ")
                break
        except:
            pass

    elem.click()
    print("Opening opportunities page. ")
    print(f"reached {driver.current_url}")

    print(f"Searching for {search_term}...")
    # search box
    search_xpath = '//*[@id="typeahead-TextSuche"]'
    search = driver.find_element(By.XPATH, search_xpath)
    search.send_keys(search_term)
    search.send_keys(Keys.ENTER)

    # # number of results
    # res_box = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, f'//*[@id="ergebniszaehler_text"]'))
    # )

    # #res_box = driver.find_element(By.XPATH, '//*[@id="ergebniszaehler_text"]')
    # try_count = 10
    # while((res := int(''.join(filter(str.isdigit, res_box.text)))) == 0 and try_count>0):
    #     time.sleep(10)
    #     #print(res)
    #     try_count-=1

    # # print(res, type(res))

    load_results()
        
    last_page_xpath = '//*[@id="page-last-bottom"]/a'
    last_page = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, last_page_xpath))
    )
    pages = int(''.join(filter(str.isdigit, last_page.text)))

    # next_btn_xpath = '//*[@id="page-next-bottom"]'
    site = driver.current_url[:-1]

    page=1
    while(page<=pages):
        if(res_count == num_of_res):
            break
        print(f"Page {page}/{pages}")            
        # elems = driver.find_elements(By.TAG_NAME, "a")
        elems = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        links = []
        find_count = res_count
        for elem in elems: 
            link = elem.get_attribute("href") 
            # print(link)
            # example: //*[@id="angebot_207798330_link"]
            if(re.search(".*/angebot/([0-9]+).*", link)):
                print("FOUND: ", link)
                links.append(link)

                find_count+=1
                if(find_count > num_of_res):
                    break

        extract_data(driver, links)
        if(res_count == num_of_res):
            break

        if(page!=pages):
            newsite = site + f"{page}"
            driver.get(newsite)
            load_results()
            print(f"reached {driver.current_url}")

            page+=1
            # next_btn = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, next_btn_xpath))
            # )
            # next_btn.click()

    print(f"reached {driver.current_url}")

    #time.sleep(5)

    driver.quit()

def load_results(driver=driver):
    # number of results
    res_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="ergebniszaehler_text"]'))
    )
    #res_box = driver.find_element(By.XPATH, '//*[@id="ergebniszaehler_text"]')
    try_count = 10
    while((res := int(''.join(filter(str.isdigit, res_box.text)))) == 0 and try_count>0):
        time.sleep(10)
        #print(res)
        try_count-=1

    # print(res, type(res))
    # return True if res!=0 else False
    # return res
        
def extract_data(driver=driver, links=[]):
    url = driver.current_url
    global res_count
    for link in links:
        driver.get(link)
        print(f"Extracting from {driver.current_url}.")
        # for _ in range(5):
        #     try:
        #         title = WebDriverWait(driver, 10).until(
        #             EC.presence_of_element_located((By.XPATH, '//*[@id="detail-seite-ueberschrift"]'))
        #             ).text
        #     except:
        #         driver.refresh()
        #         pass

        with open('edu_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            
            print("Searching for title... ")
            title = get_text(path='//*[@id="detail-seite-ueberschrift"]')
            print("Searching for dates and duration... ")
            start_date = get_text(path = '//*[@id="detail_termin_marg"]/dd[1]')
            end_date = get_text(path = '//*[@id="detail_termin_marg"]/dd[2]')
            duration = get_text(path = '//*[@id="detail_termin_marg"]/dd[3]/ba-bub-chip/div/div[2]')
            print("Searching for cost and requirements... ")
            cost = get_text(path = '//*[@id="detail_kosten_gebuehren"]/dd[1]')
            req = get_text(path = '//*[@id="detail_zuganginfo"]/dd[1]/ul')
            print("Searching for course details... ")
            ongoing = get_text(path = '//*[@id="detail_termin_marg"]/dd[4]')
            class_time = get_text(path = '//*[@id="_marg_wbinfo_uzeit"]/ba-bub-chip/div/div[2]')
            job_acc = get_text(path = '//*[@id="_marg_wbinfo_berufsbegleitend"]')
            form_of_learning = get_text(path = '//*[@id="_marg_wbinfo_uform"]/ba-bub-chip/div/div[2]')
            practical_exp =get_text(path = '//*[@id="_marg_wbinfo_praxisanteile"]')
            print("Searching for provider details... ")
            grad_type = get_text(path = '//*[@id="_marg_wbinfo_abschlussart"]/p')
            grad_name = get_text(path = '//*[@id="_marg_wbinfo_abschlussbez"]/p')
            course_link = get_text(path = '//*[@id="_marg_wbinfo_link"]/a')
            course_provider = get_text(path = '//*[@id="detail-anbieter-name"]/dd')
            school_type = get_text(path = '//*[@id="_marg_wbinfo_schulart"]')
            address = get_text(path = '//*[@id="detail-anbieter-strasse"]/dd')
            phone = get_text(path = '//*[@id="detail-anbieter-telefon"]/dd')
            email = get_text(path = '//*[@id="detail-anbieter-email"]/dd')
            website = get_text(path = '//*[@id="detail-anbieter-homepage"]/dd/a')
            print("Searching for remarks... ")
            remarks = get_text(path = '//*[@id="detail_dauer_termine"]/dd[6]/p')

            entry_list = [title, start_date, end_date, duration,
                        cost, req, ongoing,
                        class_time, job_acc, form_of_learning,
                        practical_exp, grad_type, grad_name,
                        course_link, course_provider, school_type,
                        address, phone, email, website, remarks]  

            writer.writerow(entry_list)          

        res_count += 1
        print(f"Extracted result {res_count}/{num_of_res}")
        if(res_count == num_of_res):
            return
        # print(f"reached {driver.current_url}")
    
    driver.get(url)
    # print(f"reached {driver.current_url}")

def get_text(driver=driver, path=''):
    for _ in range(wait_time):
        try:
            txt_ls = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, path))
                )
            pre_txt = ""
            for x in txt_ls:
                pre_txt += x.text

            txt = re.sub(r"[\r\n\t]+", " ", pre_txt)            
            # print("Found!")
            break
        except Exception as e:
            txt = "N/A"
            # print(f"Retrying... ({i+1}/3)")
            driver.refresh()
            pass
    
    return txt

def initialize():
    global search_term
    global num_of_res

    if(len(sys.argv)>1):
        search_term = sys.argv[1]
        num_of_res = int(sys.argv[2])

        print("Received arguments from terminal.")
    else:
        search_term = input("Enter search term: ")
        num_of_res = int(input("Enter number of results: "))

    with open("edu_data.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["Title",
                "Start Date",
                "End Date",
                "Duration",
                "Cost",
                "Requirements",
                "Ongoing Entry",
                "Class Time",
                "Job Accompanying",
                "Form of Learning",
                "Practical Experience",
                "Graduation Form",
                "Graduation Name",
                "Link",
                "Provider",
                "Type of School",
                "Address",
                "Phone",
                "Email",
                "Website",
                "Remarks"
        ]

        writer.writerow(field)

if __name__ == "__main__":
    initialize()
    main()