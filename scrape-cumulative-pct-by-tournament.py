from bs4 import BeautifulSoup
from Grid import Grid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

competions = [{"url": "https://widgets.curling.io/index.html?lang=en&apiKey=qw4LUsJ1_aQ#!/competitions/4390", "name": "2019"},
              {"url": "https://widgets.curling.io/index.html?lang=en&apiKey=qw4LUsJ1_aQ#!/competitions/3377", "name": "2018"},
              {"url": "https://widgets.curling.io/index.html?lang=en&apiKey=qw4LUsJ1_aQ#!/competitions/2182", "name": "2017"},
              {"url": "https://widgets.curling.io/index.html?lang=en&apiKey=qw4LUsJ1_aQ#!/competitions/1898", "name": "2016"}]

grid = Grid()
grid.append_row(["Competition Year", "Team", "Team Seed", "Draw", "Relative Draw", "Athlete Name", "Delivery", "Player Position", "",
                 "In Turn Draws", "Percent", "Out-Turn Draws", "Percent", "Total", "Total Percent", "",
                 "In-Turn Hits", "Percent", "Out-Turn Hits", "Percent", "Total", "Total Perent", "",
                 "In-Turns", "Percent", "Out-Turns", "Percent", "Total", "Overall Perent"]
                )

grid2 = Grid()
grid2.append_row(["Competition Year", "Team", "Team Seed", "Draw", "Relative Draw", "Athlete Name", "Delivery", "Player Position", "",
                  "In Turn Draws", "Percent", "Out-Turn Draws", "Percent", "Total", "Total Percent", "",
                 "In-Turn Hits", "Percent", "Out-Turn Hits", "Percent", "Total", "Total Perent", "",
                 "In-Turns", "Percent", "Out-Turns", "Percent", "Total", "Overall Perent"]
                 )

driver = webdriver.Chrome()
driver.implicitly_wait(30)

for competition in competions:
    print("Starting competition: " + competition["name"])
    
    #round robin seed    
    driver.get(competition["url"] + "/standings")
    driver.execute_script("window.print=function(){};") #disable print dialogue 
    
    driver.find_elements_by_class_name("curlcast-standings__button-standing-link") #wait until element is created
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    poolButtons = soup.find("div",{"class":"curlcast-standings__button"}).findAll("a")[0:2]
    seeds = {}
    
    for button in poolButtons:
        val = button["href"].split("/")[-1]
        driver.get(competition["url"] + "/standings/" + val)
        driver.execute_script("window.print=function(){};") #disable print dialogue 
        
        driver.find_elements_by_class_name("round-robin-teams__list-body-row") #wait until element is created
        
        soup = BeautifulSoup(driver.page_source, "html.parser")       
        rows = soup.find("tbody", {"class": "round-robin-teams__list-body"}).findAll("tr")
        
        for index,row in enumerate(rows):
            teamName = row.find("span", {"class":"device__not-phone"}).getText()
            seeds[teamName] = index + 1
    
    #statistics    
    driver.get(competition["url"] + "/reports/cumulative_statistics_by_team")
    driver.execute_script("window.print=function(){};") #disable print dialogue    
    
    driver.find_elements_by_class_name("reports-cumulative-statistics-by-team__selectors-team") #wait until element is created
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    teamDropdown = soup.find("div",{"class":"reports-cumulative-statistics-by-team__selectors-team"})
    teamOptions = [{"name": i.getText(), "val": i["value"]} for i in teamDropdown.findAll("option")]
    
    for team in teamOptions:
        print("\tStarting team: " + team["name"])
        
        driver.get(competition["url"] + "/reports/cumulative_statistics_by_team/" + team["val"])
        driver.execute_script("window.print=function(){};") #disable print dialogue
        
        driver.find_elements_by_class_name("reports-cumulative-statistics-by-team__selectors-draw") #wait until element is created
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        drawDropdown = soup.find("div",{"class":"reports-cumulative-statistics-by-team__selectors-draw"})
        drawOptions = [{"name": i.getText().split(" ")[2], "val": i["value"]} for i in [drawDropdown.findAll("option")[-1]]]
        
        for index,draw in enumerate(drawOptions):
                print("\t\tStarting draw: " + draw["name"])

                driver.get(competition["url"] + "/reports/cumulative_statistics_by_team/" + team["val"] + "/draws/" + draw["val"])
                driver.execute_script("window.print=function(){};") #disable print dialogue
            
                driver.find_elements_by_class_name("reports-cumulative-statistics-by-team__team-athlete-position") #wait until element is created
            
                soup = BeautifulSoup(driver.page_source, "html.parser")
                athleteContainers = soup.findAll("div",{"class":"reports-cumulative-statistics-by-team__team-athlete-container"})
                
                for athleteContainer in athleteContainers:
                    athleteName = athleteContainer.find("div", {"class":"reports-cumulative-statistics-by-team__team-athlete-name"}).getText()
                    athleteDelivery = athleteContainer.find("div", {"class":"reports-cumulative-statistics-by-team__team-athlete-delivery"}).getText()
                    
                    if athleteName == team["name"]: #if team total
                        position = "ALL"
                        athleteName = None
                        athleteDelivery = None
                    else:
                        position = athleteContainer.find("div", {"class":"reports-cumulative-statistics-by-team__team-athlete-position"}).getText()
                        if position == "":
                            position = "alternate"
                            
                    tableSections = athleteContainer.find("table", {"class":"reports-cumulative-statistics-by-team"}).findAll("tbody")
                    
                    drawRow = tableSections[1].findAll("tr")[0]
                    drawInfo = drawRow.findAll("td")
                    drawData = [i.getText() for i in [drawInfo[1], drawInfo[3], drawInfo[4], drawInfo[6], drawInfo[7], drawInfo[9]]]
                    
                    hitRow = tableSections[1].findAll("tr")[1]
                    hitInfo = hitRow.findAll("td")
                    hitData = [i.getText() for i in [hitInfo[1], hitInfo[3], hitInfo[4], hitInfo[6], hitInfo[7], hitInfo[9]]]
                    
                    totRow = tableSections[2].find("tr")
                    totInfo = totRow.findAll("td")
                    totData = [i.getText() for i in [totInfo[1], totInfo[3], totInfo[4], totInfo[6], totInfo[7], totInfo[9]]]                   
                            
                    if athleteName == None:
                        grid2.append_row([competition["name"], team["name"].split(" (")[0].lower(), seeds[team["name"]], draw["name"], index+1,athleteName, athleteDelivery, position] + [""] +
                                        drawData + [""] +
                                        hitData + [""] +
                                        totData)
                    else: 
                        grid.append_row([competition["name"], team["name"].split(" (")[0].lower(), seeds[team["name"]], draw["name"], index+1,athleteName, athleteDelivery, position] + [""] +
                                                             drawData + [""] +
                                                            hitData + [""] +
                                                            totData)                     

driver.quit()

print(grid)
print("\n\n\n")
print(grid2)
grid.toCSV("cumulative-pct-by-tournament-players.csv")
grid2.toCSV("cumulative-pct-by-tournament-teams.csv")