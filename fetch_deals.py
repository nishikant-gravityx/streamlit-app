#imports 

print("fetch script started")

import tweepy
import pandas as pd
import numpy as np
from datetime import date, timedelta
from datetime import date, timedelta

import json
import ast
from ast import literal_eval


from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import time

from io import BytesIO
import requests

import notion_df
notion_df.pandas()


#Config Parameters ,
consumer_key = "kRbg23ZpPh6c388m3zOPw4BOy"
consumer_secret =  "czpjeAJCDpHbJ2UVTO8DiWBC5T9dLl7zLEZ25x1RuTZFB0Farj"
access_token = "1401250141479194625-jTCUxSS3csjEOdq6VTo2EK20kwJJhE"
access_token_secret = "hZcy0rZ1Dr6Ue20D7UX5CzxTWcu5v2vUEJF8jVUP1MR80"
bearer_token="AAAAAAAAAAAAAAAAAAAAAAU%2FewEAAAAA0v0eR04tZFL6hIfZhElBbmh3iR8%3DReKt2wIap7FPGbXpY38GH9oqlHLho9uLqtTwDSRfgTMgfHyqag"
bearer_token_an="AAAAAAAAAAAAAAAAAAAAABdZiQEAAAAA1Au1hPs%2BsdGAVC8TDmKtZsBVUcE%3DChMoAGlcxEmWIKzKr2rGAU5Xt2YeifIwERRZogtRCkn6Pc8fkQ"
bearer_token_gx="AAAAAAAAAAAAAAAAAAAAADlZiQEAAAAAB5X7V9v0lbqvjnKmaPFVWpbO3bE%3Dhq9akUBeCl7vWKC27LklBOVSO3q64FwP53Co46bEJGMkxtuk8n"
bearer_token_vy="AAAAAAAAAAAAAAAAAAAAAO9aiQEAAAAA8FEVNJ7CIxB9KbfDgYNXBRALreU%3DCwbuyJfYADoj91fq7JfDwFpiG1RZnIHAG3zjEuZMtM27tsfg3w"
bearer_token_nkx="AAAAAAAAAAAAAAAAAAAAAOOGiQEAAAAA86eXGz%2FiLLbHXezROPlicrq4mU4%3Duat48JMMTerECjoFt440A6lXXME0E9qI8lMwjprYLCDPp8L2XW"
bearer_token_list=[bearer_token,bearer_token_an,bearer_token_gx,bearer_token_vy,bearer_token_nkx]
# tg_chat_id="@dealflowtest"
tg_chat_id="-1001539278724"
tg_bot_token="5452504081:AAEE0f7c4X1aa1cHByKp_TIBcFPZb8KrPiI"
# sheet_key="1kTVSyil9sdpLy9vUSPRIOEXLoLxzXQk2CNYOisBDTtw"
# sheet_key="16NyQaoXbhFFz5e19ZYgpIDXtxJqXfWLinnDVRjgp21w"#vc subset updated list
sheet_key="1QlSIspEWqFTL4D89Gl3x8k1ymxRZ8FTdbdCQtSHsHbQ"#biggest_list_updated
# sheet_key="1qk6Qn7DAVEvJSmrlclGHyIoNujaXoHe2BsZsO0lNFxE" #Tier_included_test_sheet
# sheet_key="1BwTE-XVOO33Q46DeGBppU1zXkpHxZFdugZrxFQslHck"#15namessheet
notion_page_url = "https://www.notion.so/510f6a137fad4a289c93951130905fb3?v=ca714f4225f746e689b7ba108880661e"
notion_api_key = "secret_8fk5mpNGVbY433QuCICIbgRa5VQeuAPDTgN5V3p1ERW"



#Label for Categorization
DeFi =["DeFi","stablecoin","money market","impermanent loss","single side staking","borrowing","lending","exchange",
       "staking","yield","liquidity","AMM","automated market maker","aggregator","dexes","liquid staking","CDP",
       "Bridge","Derivatives","Algo-stables","Yield aggregator","synthetics","launchpad","bonds",
       "reserve currency","options","perpetuals","long","short","indexes","payments","leverage",
       "NFT collateralization","RWA","undercollateralized","market making","loan","liquidation","interest","governance"]

NFT=["NFT","art","ERC-721","ERC-1155","Non fungible tokens","SBT","NFTs","metaplex","opensea","magic eden","bayc","mayc"]

ZK=["ZK","ZKP","zero knowledge","ZKPs","zero-knowledge","zkevm","starks","snarks","hermez","succint","starkware","zksync","zklink"
   "zk proof","zk-SNARKS", "zk-STARKS","zk-SNARGS","Bulletproofs","zk Rollups", "zkapps","recusrive ZK","scroll labs"]

GameFi=[ "Game","metaverse","verse","meta","3D","avatars","AAA","studio","play2earn","move2earn","gaming","play"
       "3D","AAAA","poker","cards","gameplay","meta","verse","2D","sink","skins"]

Infra=["compute","storage","internet","iot","music","video","node","RPC","rollup" ,"execution" ,"modular"
      ,"sidechain","modular execution","blockchain","layer" ,"data avail" ,"sharding","layer2","L2","optimistic rollup","zk rollup",
     "SDK","API","node","RPC" ,"code" ,"coding" ,"audit","layer1","evm" ,"cosmwasm" ,"move" ,"rust" ,"protocol"
     "smart contracts","solidity","nonevm","move","privacy","private","computing","launching","platform","tooling"
      "toolset","suite","web3","web3 native","wallet","noncustodial","seed phrase","protocol","simulation","transactions","proof of"]

Data=["data","indexing","analytics","oracle","feeds","onchain","indexers","graphs","subgraphs","graphQL","SQL",
      "big data","metrics"]

Individual=["CEO","Cofounder","dev","developer","buildoor","founder","learning","investing","investor" ,"account","GP","analyst"
           "building","builder","focused","creator", "creating", "founded","contributor","contributing","VC","running","researching","programmer","coder",
            "coding","hosting","shitposting","posting","legal","markeing","CMO","CFO","COO","executive","manager"
           "product","designer","graphic designer","UI/UX designer","engineer","engineering","designing"
           "playing", "I'm","me","girl","boy","married","father","son","daughter","i","am","teaching"]



#defining user_names to fetch_data about
#Adding user from Excel
def get_usernames_sheets(sheet_key):
    r = requests.get('https://docs.google.com/spreadsheet/ccc?key='+sheet_key+'&output=csv')
    data = r.content
    df = pd.read_csv(BytesIO(data))
    usernames=list(df["usernames"])
    print("VC_check",df["vcs"][9])
    return df,usernames

#getting_users_id
# def get_users_id(usernames):
#     user = x.get_users(usernames=usernames,user_fields=["description","url"])
#     id_list=[]
#     for i in range(len(usernames)):
#         print(i)
#         id_list.append(user["data"][i].get("id"))
#     return id_list

def get_users_id(usernames):
    id_list=[]
    for k in range(0, len(usernames), 100):
        newlist=usernames[k:k+100]
        print("newlist",len(newlist))
        user = x.get_users(usernames=newlist,user_fields=["description","url"])
        for i in range(len(newlist)-3):
            print("i",i)
            print(len(user))
            id_list.append(user["data"][i].get("id"))     
    return id_list



#fetching following info for all users
def fetch_users_following(id_list,bearer_token,x,sheet_df,bearer_token_list):
    output=pd.DataFrame()
    count = 0 
    user_count=0
    for i in id_list:
        count+=1
        print("id count "+str(count))
        if(count%75==0):
            print("reached 5 limits")
            time.sleep(900)
            count=1
            x=tweepy.Client(bearer_token,return_type=dict)
        if(count%15==0):
                bearer_token_next=bearer_token_list[round((count)/15)]
                print(count,bearer_token_next)
#                 time.sleep(900)
                x=tweepy.Client(bearer_token_next,return_type=dict)
#                 count=0
        n = x.get_users_following(id=i, user_fields=["description","created_at","public_metrics"],max_results=100)
        print("user_count ***",user_count)
        for y in n:
                for j in n[y]:
                    if(type(j)==dict):
                        if 'resource' in j.keys():
                            j.clear()
                        if 'errors' in j.keys():
                            j.clear()
                        if 'title' in j.keys():
                            j.clear()
                        else:
                            tier=sheet_df["tier"][user_count]
                            vc=sheet_df["vcs"][user_count]
                            catg=get_category(j["description"])
                            print(user_count,tier,vc)
                            dict1 = {'tier':tier,'category':catg,"VC":vc} 
                            j.update(dict1)
                            print(j)
                output = output.append(n[y], ignore_index=True)
        user_count=user_count+1
#                 break
#         for i in n:
#             output = output.append(n[i], ignore_index=True)
#             break
    print(type(output.public_metrics))
    output["created_at"] = pd.to_datetime(output["created_at"], format='%Y-%m-%d')
    output["detected_at"]= date.today()
    output.to_csv("testoor.csv",index=False)
    output=pd.read_csv("testoor.csv")
    output.public_metrics = output.public_metrics.fillna('{}') 
    output.public_metrics = output.public_metrics.apply(literal_eval)
    output = output.join(pd.json_normalize(output.pop('public_metrics')))
    output=output.loc[(output["created_at"]>=str(date.today()-timedelta(days=300)))]
    output=output.drop_duplicates(keep="first",subset="username")
    # output2.to_csv("main.csv",mode="a",header=False)
    #checking in for duplicates with main csv
    old=pd.read_csv("main.csv")   
    new_acc=output[~output.username.isin(main.username)]
    old=pd.concat([old,new_acc],axis=0,ignore_index=True)
    old_to_csv("main.csv",index=False)
    # old=old.append(new_acc)
    # old.to_csv("main.csv",mode="a",header=False,index=False)
    new_acc.to_csv(str(date.today())+'.csv',index=False)
    return output2
    

    
#old-yesterday, new=today #difference -> new accounts
def get_new_following():
    old=pd.read_csv(str(date.today()-timedelta(days=7))+'.csv')
    new=pd.read_csv(str(date.today())+'.csv')
    final=new[~new.id.isin(old.id)]
    new_acc=final["username"].tolist()
    return new_acc
    
    

def post_tg_bot(new_acc,tg_chat_id):
    updater = Updater(tg_bot_token,use_context=True)
    print(new_acc)
    count = 0 
    for i in new_acc:
            count+=1
            if(count>19):
                time.sleep(60)
                count=0
            else:
                updater.bot.sendMessage(chat_id=tg_chat_id, text="https://www.twitter.com/"+i)
                
def post_to_notion(deals_df,notion_page_url,notion_api_key):
#     deals_df = pd.read_csv("test_7_aug.csv")
    deals_df=deals_df[["created_at","name","username","description","tier","category"]]
    # df.to_notion(page_url, api_key=api_key)
    notion_df.upload(deals_df,notion_page_url, title="deals-details", api_key=notion_api_key)
            
    
#Getting Tier based on Id
# def get_tier(sheet_df,username):
#     tier=sheet_df["Tier"].loc[sheet_df['Username'] == username]
#     return tier

#Getting Category based on Id
def get_category(desc):
    desc=str(desc)
    if  any(x in desc.lower() for x in DeFi):
         return "DeFi"
    if  any(x in desc.lower() for x in Infra):
        return "Infra"
    if any(x in desc.lower() for x in ZK):
        return "ZK"
    if  any(x in desc.lower() for x in Data):
        return "Data"
    if  any(x in desc.lower() for x in NFT):
        return "NFT"
    if any(x in desc.lower() for x in GameFi):
        return "GameFi"
    if  any(x in desc.lower() for x in Individual):
        return "Individual"
    else:
        return "Not Specified"



#Main Function

if __name__ == "__main__" :
    x=tweepy.Client(bearer_token,return_type=dict)
    sheet_df,usernames=get_usernames_sheets(sheet_key)
    id_list=get_users_id(usernames)
    deals_df=fetch_users_following(id_list,bearer_token,x,sheet_df,bearer_token_list)
#     new_acc=get_new_following()
#     post_to_notion(deals_df,notion_page_url,notion_api_key)
#     post_tg_bot(new_acc,tg_chat_id) 


