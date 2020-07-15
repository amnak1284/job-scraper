#scraper that gets jobs from indeed
# for now just make default be SF
import webbrowser, bs4, requests, sys, csv



progarg =  sys.argv[1:]
progarg =[i.strip(',') for i in progarg] 
print(progarg)
skills = "%20".join(progarg)
print(skills)

resp = requests.get('https://www.indeed.com/jobs?q='+ skills +'&l=San%20Francisco%2C%20CA')
resp.raise_for_status()


jobs = bs4.BeautifulSoup(resp.text, 'html.parser')

type(jobs)
all_job_cards = jobs.select('body')
len(all_job_cards)

all_j = jobs.find_all('div', attrs={"class":"jobsearch-SerpJobCard unifiedRow row result"})
print(len(all_j))
i = 0
j = 0
k = 0
job_array = []
for tag in all_j:
    job_title_tags = tag.find_all("h2", {"class":"title"})
    job_company = tag.find_all("div", {"class":"sjcl"})

    description_tag = tag.find_all("div", {"class": "summary"})

    for tag in job_title_tags:
        title = tag.text.strip()
        title = title.strip('/nnew')
        title = title.strip() 

        job_array.append({'title': title})
    
    for comp in job_company:
        company = comp.find_all("a", {"data-tn-element": "companyName"})
        for c in company:

            comp = c.text.strip()
            comp = comp.strip('/nnew')

            job_array[i]["company"] = comp
            i = i + 1
    for loc in job_company:
        location = loc.find_all("span", {"class": "location accessible-contrast-color-location"})
        for l in location:

            loc = l.text.strip()
            loc = loc.strip('/nnew')

            job_array[k]["location"] = loc
            k = k + 1

    for desc in description_tag:
        description = desc.text.strip()
        description = description.strip('/nnew')
        d = description.split('.')
        d = [nl.strip() for nl in d]
        description = ' '.join(d)
        job_array[j]["description"] = description
        j = j + 1


        #Creating a csv for results
value = 0
print(job_array)
with open('Jobs.csv', mode='w') as csv_file:
    fieldnames = ['title', 'company', 'location', 'description']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for rows in job_array:
        writer.writerow({'title': rows.get('title'), 'company': rows.get('company'), 'location': rows.get('location'), 'description': rows.get('description')})
        value = value + 1
