import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

URL = "https://www.ktunotes.in/ktu-2019-new-scheme-notes/"

options = Options()

options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--enable-unsafe-swiftshader")
options.add_argument("--no-sandbox")
options.add_argument("--disable-pop-blocking")


driver = webdriver.Chrome(options=options)


async def extract_gdrive_url(sub_name: str, sem_num: str, subject: str) -> list[str]:
    driver.get(URL)
    try:
        try:
            sem_h1_tags = driver.find_elements(
                By.CLASS_NAME, "elementor-icon-box-title"
            )
            sem_a_tags = [tag.find_element(By.TAG_NAME, "a") for tag in sem_h1_tags]
            required_a_tag = [tag for tag in sem_a_tags if tag.text == sem_num][0]
            if not required_a_tag:
                print("Semester not found")
            driver.get(required_a_tag.get_attribute("href"))
        except NoSuchElementException as e:
            print(e)
        except IndexError as e:
            print(f"[ERROR] in sem number identification {e}")
            print(sem_a_tags)

        if int(sem_num[1]) >= 3:
            try:
                dept_h1_tags = driver.find_elements(
                    By.CLASS_NAME,
                    "elementor-icon-box-title",
                )
                if dept_h1_tags == 0:
                    print("Department List not found")
                dept_a_tags = [
                    tag.find_element(By.TAG_NAME, "a")
                    for index, tag in enumerate(dept_h1_tags)
                    if index != 2
                ]
                if len(dept_a_tags) == 0:
                    print("Department link tags not found")
                required_tag = [tag for tag in dept_a_tags if tag.text == subject][0]
                if not required_tag:
                    print("Department not found")
                driver.get(required_tag.get_attribute("href"))
            except NoSuchElementException as e:
                print(f"[ERROR] {e}")
            except IndexError as e:
                print(f"[ERROR] in department identification {e}")

        sem_name_tags = driver.find_elements(By.CLASS_NAME, "elementor-button")
        if len(sem_name_tags) == 0:
            print("Subject name tags not found")
        required_name_tag = [
            tag
            for tag in sem_name_tags
            if tag.find_element(By.CLASS_NAME, "elementor-button-text").text == sub_name
        ][0]
        if not required_name_tag:
            print("Subject name not found")
        driver.get(required_name_tag.get_attribute("href"))

        gdrive_tags = driver.find_elements(By.CLASS_NAME, "elementor-button")
        gdrive_links = [
            {
                tag.find_element(
                    By.CLASS_NAME, "elementor-button-text"
                ).text: tag.get_attribute("href")
            }
            for tag in gdrive_tags
        ]
        return gdrive_links
    except Exception as e:
        print(e)
    except NoSuchElementException as e:
        print(f"[ERROR] {e}")
    except IndexError as e:
        print(f"[ERROR] in subject identification {e}")
