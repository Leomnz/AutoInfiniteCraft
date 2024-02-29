import atexit
import random
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from collections import deque
import re
from itertools import combinations

import undetected_chromedriver as uc

from element import Element
import graph_visualization

# STARTUP
game_url = "https://neal.fun/infinite-craft/"

browser = uc.Chrome()
wait = WebDriverWait(browser, timeout=20)
browser.set_window_size(1920, 1080)

browser.get(game_url)
assert 'Infinite Craft' in browser.title

wait.until(lambda driver: driver.find_element(By.CLASS_NAME, 'items'))
items_container = browser.find_element(By.CLASS_NAME, 'items')


def get_element_from_div(div, item=True):
    if item:
        emoji = div.find_element(By.CLASS_NAME, 'item-emoji').text
    else:
        emoji = div.find_element(By.CLASS_NAME, 'instance-emoji').text
    name = re.sub(rf"{emoji}", '', div.text).strip()
    # print(f"Found {name} with emoji {emoji}")
    return Element(name, emoji)


unlocked_elements = set()
for item in items_container.find_elements(By.CLASS_NAME, 'item'):  # init unlocked elements
    current_element = get_element_from_div(item)
    unlocked_elements.add(current_element)
    current_element.add_to_graph()

completed_combos = set()  # completed or currently queued combinations
q = deque()  # queue of combinations to try


def exit_handler():
    browser.quit()
    graph_visualization.draw_graph()
    graph_visualization.save_graph()


atexit.register(exit_handler)


# MAIN

def get_new_combos():  # get all possible combinations of unlocked elements
    for combo in list(combinations(unlocked_elements, 2)):
        if combo not in completed_combos:
            completed_combos.add(combo)
            q.append(combo)


def combine(element1: Element, element2: Element):  # combine two elements
    div1 = WebDriverWait(browser, timeout=20).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{element1.name}')]"))
    )
    div2 = WebDriverWait(browser, timeout=20).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{element2.name}')]"))
    )

    def drag_and_drop(element):
        actions = ActionChains(browser)
        actions.move_to_element(element).click_and_hold().perform()

        actions = ActionChains(browser)
        container = browser.find_element(By.CSS_SELECTOR, ".container")
        actions.move_to_element(container).perform()

        actions = ActionChains(browser)
        actions.move_to_element(container).release().perform()
        container.click()

    drag_and_drop(div1)
    drag_and_drop(div2)

    # find the result, class=instances
    instance_container = WebDriverWait(browser, timeout=20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'instances'))
    )

    def resulting_child(parent):
        children = parent.find_elements(By.CLASS_NAME, 'item')
        children = [child for child in children if 'instance-hide' not in child.get_attribute('class')]
        if len(children) == 1:
            return children[0]
        else:
            return None

    # wait until there is only one child that is not hidden
    wait.until(lambda driver: resulting_child(instance_container) is not None)
    result = resulting_child(instance_container)

    result_element = get_element_from_div(result, item=False)
    result_element.set_parents(element1.name, element2.name)
    result_element.add_to_graph()
    unlocked_elements.add(result_element)
    print(
        f"Combined {element1.emoji} {element1.name} and {element2.emoji} {element2.name} to get {result_element.emoji} {result_element.name}")

    sleep(random.uniform(0.5, 2))
    clear_button = browser.find_element(By.CLASS_NAME, 'clear')
    clear_button.click()


depth = 3
for i in range(depth):
    get_new_combos()
    print(f"Depth: {i}")
    print(f"Unlocked Elements: {unlocked_elements}")
    print(f"Queue: {q}")
    print(f"Completed Combos: {completed_combos}")
    while q:
        current_combo = q.popleft()
        combine(*current_combo)
        sleep(random.uniform(0.5, 2))

# END
browser.quit()
graph_visualization.draw_graph()
