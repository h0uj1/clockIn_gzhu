import time

import selenium.webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def wd_login(xuhao, mima):
    options = Options()
    optionsList = [
        "--headless", "--disable-gpu", "--window-size=1920,1200",
        "--ignore-certificate-errors", "--disable-extensions", "--no-sandbox",
        "--disable-dev-shm-usage"
    ]

    # optionsList = [
    #     "--disable-gpu", "--window-size=1920,1200",
    #     "--ignore-certificate-errors", "--disable-extensions", "--no-sandbox",
    #     "--disable-dev-shm-usage"
    # ]
    for option in optionsList:
        options.add_argument(option)

    options.page_load_strategy = 'eager'
    options.add_experimental_option("excludeSwitches", ['enable-logging'])

    driver = selenium.webdriver.Edge(service=Service(
        EdgeChromiumDriverManager().install()),
                                     options=options)

    driver.get(
        f'https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fnewmy.gzhu.edu.cn%2Fup%2Fview%3Fm%3Dup'
    )

    try:
        # 智能等待
        WebDriverWait(driver, 30, 0.5).until(
            ec.visibility_of_element_located(
                (By.XPATH, "//div[@class='robot-mag-win small-big-small']")))
    except:
        pass

    driver.find_element(By.ID, 'un').send_keys(xuhao)
    driver.find_element(By.ID, 'pd').send_keys(mima)
    driver.find_element(By.ID, 'index_login_btn').click()

    try:
        WebDriverWait(driver, 30, 0.5).until(
            ec.visibility_of_element_located(
                (By.XPATH, '//a[@title="健康打卡"]/img')))
    except:
        pass

    driver.find_element(By.XPATH, '//a[@title="健康打卡"]/img').click()

    title = driver.title
    if title == "融合门户":
        driver.close()
        windows = driver.window_handles
        driver.switch_to.window(windows[0])

    print('登录融合门户成功！')

    try:
        WebDriverWait(driver, 30, 0.5).until(
            ec.visibility_of_element_located(
                (By.XPATH, "//img[@title='查看办事指南']")))
    except:
        pass

    jumpButton = driver.find_element(By.XPATH, "//img[@title='查看办事指南']")
    ActionChains(driver).move_to_element(jumpButton).click().perform()

    title = driver.title
    if title == "服务大厅":
        driver.close()
        windows = driver.window_handles
        driver.switch_to.window(windows[0])

    print('登录服务大厅成功！')

    try:
        WebDriverWait(driver, 30, 0.5).until(
            ec.visibility_of_element_located(By.XPATH,
                                             "//div[@style='display:none;']"))
    except:
        pass

    time.sleep(20)

    startButton = driver.find_element(By.XPATH,
                                      "//a[contains(text(), '开始上报')]")
    ActionChains(driver).move_to_element(startButton).click().perform()

    print('登录打卡开始界面成功！')

    try:
        WebDriverWait(driver, 30, 0.5).until(
            ec.visibility_of_element_located(
                By.XPATH, "//font[contains(text(), '正常')]/../../input[1]"))
    except:
        pass

    time.sleep(20)

    lastbutton = driver.find_element(
        By.XPATH, "//div[@align='right']/input[@type='checkbox']")
    ActionChains(driver).move_to_element(lastbutton).click().perform()

    driver.find_element(By.XPATH, "//nobr[contains(text(), '提交')]/..").click()

    try:
        WebDriverWait(driver, 10, 0.5).until(
            ec.visibility_of_element_located(
                By.XPATH, "//button[contains(text(), '确定')]"))
    except:
        pass

    driver.find_element(By.XPATH, "//button[contains(text(), '确定')]").click()

    time.sleep(10)

    formErrorContentList = driver.find_elements(By.XPATH,
                                                "//div[@class='line10']")

    for formErrorContent in formErrorContentList:
        button = driver.find_elements(
            locate_with(By.XPATH,
                        "//input[@type='radio']").below(formErrorContent))[0]
        ActionChains(driver).move_to_element(button).click().perform()

    driver.find_element(By.XPATH, "//nobr[contains(text(), '提交')]/..").click()

    try:
        WebDriverWait(driver, 10, 0.5).until(
            ec.visibility_of_element_located(
                By.XPATH, "//button[contains(text(), '确定')]"))
    except:
        pass

    time.sleep(10)

    driver.find_element(By.XPATH, "//button[contains(text(), '确定')]").click()

    print('打卡成功！')


if __name__ == "__main__":
    xuhao = input("学号：")
    mima = input("密码：")
    wd_login(xuhao, mima)