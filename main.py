from selenium import webdriver
import time

# Dikkat: Sitedeki id'ler hep degisiyor.
Url = "https://yoksis.yok.gov.tr/websitesiuygulamalari/harita/"

AllUniversity = []
switcher = {
    0: "Ad",
    1: "Website",
    2: "Eposta",
    3: "Telefon",
    4: "Fax",
    5: "Adres",
}

# Butun Selector ler
TumUniversitesiListesi_ButtonClass = "btn-danger"
ShadowWindow_DivClass = "z-window-shadow"
Rows_TrClass = "z-listitem"
RowContent_DivClass = "z-listcell-content"
Next_AtagClass = "z-paging-next"

def getNextPage(secretWindow):
    print("Go to Next Page")
    nextLink = secretWindow.find_element_by_class_name(Next_AtagClass)
    status = nextLink.get_attribute("disabled")
    if status == None:
        nextLink.click()
        time.sleep(5)
        return "Okey"
    return status

def getUniversityInShadowWindow(secretWindow):
    print("Get University Contents")
    trElements = secretWindow.find_elements_by_class_name(Rows_TrClass)
    for trElement in trElements:
        University = {}
        contents = trElement.find_elements_by_class_name(RowContent_DivClass)
        for index, content in enumerate(contents):
            University[switcher.get(index)] = content.text
        print(University)
        AllUniversity.append(University)

def main():
    print("Started Selenim Code")
    # Site acildi.
    driver = webdriver.Chrome()
    driver.get(Url)
    time.sleep(5)

    # Tum UniversiteListesi buttonuna tiklanildi. 
    element = driver.find_element_by_class_name(TumUniversitesiListesi_ButtonClass)
    element.click()
    time.sleep(5)

    # Gizli pencere yakalandi.
    secretWindow = driver.find_element_by_class_name(ShadowWindow_DivClass)
    
    getUniversityInShadowWindow(secretWindow)
    while "Okey" == getNextPage(secretWindow):
        getUniversityInShadowWindow(secretWindow)

    print(AllUniversity)
    a = input("Exit: ")
    driver.quit()

if __name__ == "__main__":
    main()