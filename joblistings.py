import requests   
import unicodecsv as csv  
from bs4 import BeautifulSoup   
  
  
# ENGINEERING JOBS  
def engineering_jobs(url):  
    result_set = []  
    soup = BeautifulSoup(requests.get(url).text)  
    listing = soup.find("div",{"class":"vacansia"})  
    table = listing.find("table")  
    for tr in table.find_all("tr")[2:]:  
        tr_list = []  
        for td in tr.find_all("td"):  
            tr_list.append(td.contents[0])  
        result_set.append(tr_list)  
    return result_set  
  
  
def jobs(url):  
    result_set = []  
    soup = BeautifulSoup(requests.get(url).text)  
    # listing = soup.find("div",{"class":"vacansia"})  
    tables = soup.find_all("table")  
    table = tables[0]  
    for tr in table.find_all("tr")[1:]:  
        tr_list = []  
        for td in tr.find_all("td"):  
            try:  
                tr_list.append(td.contents[0])  
            except IndexError:  
                tr_list.append(td.contents)  
        result_set.append(tr_list)  
    return result_set  
  
  
def parse_engineering(result_set):  
    rows = []   
    for result in result_set:  
        title_children = result[0].children  
        note = result[2]  
        title = [t for t in title_children]  
        price = ''.join(s for s in result[1].split() if s.isdigit())  
        rows.append((price,title[0],note))  
    return rows   
  
  
def parse_jobs(result_set):  
    rows = []   
    for result in result_set:  
        title = result[1]  
        note = result[2]  
        price = ''.join(s for s in result[2].split() if s.isdigit())  
        rows.append((price,title,note))  
    return rows   
  
  
def csv_output(rows,filename):  
    with open(filename, "wb") as f:  
        writer = csv.writer(f)  
        for row in rows:  
            row = list(row)  
            # row[0] = row[0].encode('utf-8')  
            writer.writerow(row)  
  
  
  
  
if __name__ == "__main__":  
    jobs_url = "http://admship.ru/?p=546"  
    job_rows = parse_jobs(jobs(jobs_url))  
    engineering_url = "http://admship.ru/?page_id=503"  
    e_rows = parse_engineering(engineering_jobs(engineering_url))  
    csv_output(e_rows,"engineering_jobs.csv")  
    csv_output(job_rows,"jobs.csv")  