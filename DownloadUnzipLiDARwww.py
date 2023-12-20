#-------------------------------------------------------------------------------
# Name:        DownloadUnzipLidarWWW
# Purpose:     Downloads and then unzips data from the Pasda www site
#
# Author:      James O'Brien
#
# Created:     Dec 20, 2023
# Copyright:   (c) James 2023
#-------------------------------------------------------------------------------


#code created from a stub built on chatgpt input
import zipfile
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from os.path import join, exists, basename, isdir


def unzip(zipFile, unzipLocation):
    zip_ref = zipfile.ZipFile(zipFile, 'r')
    zip_ref.extractall(unzipLocation)
    zip_ref.close()

def download_files_with_wildcard(base_url, wildcard, download_path,unzippedLidarFolder):
    
    response = requests.get(base_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links that match the wildcard pattern
        matching_links = [urljoin(base_url, link.get('href')) for link in soup.find_all('a') if wildcard in link.get('href')]
        
        ## here's the same line of code as above without list comprehension
        # matching_links = []        
        # for link in soup.find_all('a'):
        #     #print("{} {}".format(wildcard,link.get('href')))
        #     if wildcard in link.get('href'):
        #         print("searching")
        #         matching_links.append(urljoin(base_url, link.get('href')))
        #         #print(matching_links)
        # Download each matching file
        for link in matching_links:
            filename = link.split("/")[-1]
            print(f"Downloading {filename}...")
            file_response = requests.get(link)
            
            # Check if the file request was successful
            if file_response.status_code == 200:
                with open(join(download_path,filename), 'wb') as file:
                    file.write(file_response.content)                
                unzip(join(download_path,filename), unzippedLidarFolder)
                print(f"{filename} downloaded successfully.")
            else:
                print(f"Failed to download {filename}. Status code: {file_response.status_code}")
    else:
        print(f"Failed to access {base_url}. Status code: {response.status_code}")


def main():
    # Example usage:
    base_url = "https://www.pasda.psu.edu/download/psu_opp/2017Orthophotos/LIDAR/DEM"
    wildcard_pattern = "227"  
    # edit these variables to the paths you want to use your computer
    download_path = r'C:\Users\jao160\Documents\Teaching_PSU\Geog489_Sp1_24\Lesson 1\DownloadLidar'
    unzippedLidarFolder = r'C:\Users\jao160\Documents\Teaching_PSU\Geog489_Sp1_24\Lesson 1\unzippedLidar'
    
    # make sure the folders exist
    for f in [download_path, unzippedLidarFolder]:
        if not exists(f):
            mkdir(f)
    
    download_files_with_wildcard(base_url, wildcard_pattern, download_path,unzippedLidarFolder)


if __name__ == '__main__':
    main()
