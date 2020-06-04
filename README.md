# twlottomldl
My part-time experimental project. Using machine learning and deep learning to predict lottery winning numbers.\
- Kick-off: 2020/05/11
- For details, please visit my project journal on HackMD: [Project Journal - Taiwan Lottery Machine Learning (twlottomldl)](https://hackmd.io/@StanS/twlottomldl)
## Snapshot 
- Purpose: Predict winning numbers of Taiwan lottery by ML/DL 
- Language: Python
- Techniques: 
    - Web scraping: requests, pyquery
    - ETL : pandas(local machine)
    - EDA :  numpy, pandas, matplotlib, Tableau
    - Modeling: (TBD)
    - WebApp Deployment: (TBD, maybe Google APP engine)
- Data:
    - Historical lottery data
    - Weather data
- Link:
    - [Project_Journal _twlottomldl](https://hackmd.io/@StanS/twlottomldl)
    - [GitHub_Repo_twlottomldl](https://github.com/stansuo/twlottomldl)
## Approach/ Strategy (Outline of Stages)
- **Stage 0: Background Survey**
	- Learn lottery rules
	- Survey available data source of winning number & weather (& moon phases)

- **Stage 1: Web Scraping**
	- Get desired weather data
	- Get desired historical lottory data

- **Stage 2: ETL (Extract, Transform, Load)**
	- Extract & correctly combine the datasets in hand.
- **Stage 3: EDA (Exploratory Data Analysis)**
	- Explore data characteristics
	- pandas, matplotlib, seaborn
	- Tableau
- **Stage 4: Modeling**
	- Divide Training/Testing Datasets
	- Train/Test different ML/DL for better prediction

- **Stage 5: WebApp Deployment**
    - Wrap the model into a usable application
    - Deploy the APP on the web
