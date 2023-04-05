from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


class Driver:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options)

        self.wait = WebDriverWait(self.driver, 30)
        self.driver.set_script_timeout(180)

    def close(self):
        self.close()

    def get_page(self, asset_id):
        self.driver.get(f'http://localhost:8000/player/{asset_id}')
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button___2vx0y")))
        self.wait_until_scene_rendered()

    def get_attributes(self):
        attributes_list = []

        allowed_names = [
            'BODY',

            'LARGE TOSS PILLOW SET',
            'LARGE TOSS PILLOW SET - 2',
            'LARGE TOSS PILLOW SET - 3',
            'LARGE TOSS / KIDNEY PILLOW SET',
            'LARGE KIDNEY PILLOW SET',
            'LARGE TOSS PILLOW',
            'MEDIUM TOSS PILLOW SET',
            'MEDIUM TOSS PILLOW SET - 2',
            'MEDIUM TOSS PILLOW SET - 3',
            'MEDIUM TOSS / KIDNEY PILLOW SET',
            'MEDIUM KIDNEY PILLOW SET',
            'MEDIUM TOSS PILLOW',
            'KIDNEY',
            'SMALL TOSS PILLOW SET',
            'SMALL TOSS PILLOW SET - 2',
            'SMALL TOSS PILLOW SET - 3',
            'SMALL TOSS PILLOW',
            'BOLSTER',
        ]

        res = self.driver.execute_script("""
        let objSnapshot = {};
        let objConfig = {};

        let confPlayer = await playerApi.getConfigurator();
        let listAttribute = confPlayer.getDisplayAttributes();

        return listAttribute
        """)

        """attributes = []

        for attribute in res:
            attributes.append(attribute['name'])"""

        for attribute in res:
            if attribute['name'] in allowed_names:
                attributes_list.append(attribute)
        return attributes_list

    def wait_until_scene_rendered(self):
        self.driver.execute_async_script(
            """
            var callback = arguments[arguments.length - 1];
            playerApi.on("rendered", function() {
                callback();
            });
            """)
