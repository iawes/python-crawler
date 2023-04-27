from selenium import webdriver
# 创建chrome选项
chrome_options = webdriver.ChromeOptions()

# 启用无头模式
chrome_options.add_argument('--headless')

# 创建webdriver实例
#service = Service(executable_path="~/chrome/chromedriver")
#browser = webdriver.Chrome(options=chrome_options, executable_path="/home/iawes/chrome/chromedriver")
driver = webdriver.Chrome(options=chrome_options)

# 创建一个Chrome浏览器对象
#driver = webdriver.Chrome()

# 访问雪球网站登录页面
driver.get("https://xueqiu.com/")

# 等待页面加载完成
driver.implicitly_wait(10)

# 点击登录按钮，打开登录框
#login_button = driver.find_element_by_xpath("//a[@data-nav='登录/注册']")
login_button = driver.find_element_by_xpath("//a[@data-analytics-data='登录']")
login_button.click()

# 输入用户名和密码
username_input = driver.find_element_by_xpath("//input[@name='username']")
username_input.send_keys("18616801636")
password_input = driver.find_element_by_xpath("//input[@name='password']")
password_input.send_keys("Asd.1234")

# 点击登录按钮，提交登录表单
submit_button = driver.find_element_by_xpath("//button[@data-type='submit']")
submit_button.click()

# 等待登录成功并跳转到首页
driver.implicitly_wait(10)

# 获取cookie
cookie = driver.get_cookies()

# 输出cookie
print(cookie)

# 关闭浏览器
driver.quit()
