#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')

import hvplot.pandas


# In[2]:


if 'data' not in pn.state.cache.keys():

    df_original = pd.read_csv('all_recipes_final.csv')

    pn.state.cache['data'] = df_original.copy()

else: 

    df_original = pn.state.cache['data']
    
    


df = df_original.copy()


# In[3]:


df = df.drop_duplicates().reset_index(drop=True)


# In[4]:


#df.columns


# In[ ]:





# In[5]:


non_veg_tags = ['beef', 'fish','lamb','lambs', 'mutton','meatball','meatballs','pork','poultry', 'sausage',
                'sausages','seafood', 'chicken','wings','meat','salmon','salmons','cob','cobs',
                'ham','pork','kebab','kebabs','snake','gosht','bacon','mutton','lamb','egg','eggs',
               'shrimp', 'shrimps','seafood','buffalo','calf','horse','moose','rabbit','turtle','duck',
                'liver','goose','turkey','jamon','salami','venison','boar','bison','pheasant',
               'prawn','tuna','bass','catfish','caviar','clam','clams','crab','crabs','hot dog','hotdog','Flounder',
                'Lobster', 'lobsters', 'mussel','Mussels','octopus','quail','Scallops', 'Oyster', 'oysters',
                'shark','Smelt','squid','swordfish','Tilapia','Trout','Whitefish','Whiting' ,'steak','veal',
                'Ribs','Brisket', 'lasagna']
non_veg_tags = [i.lower() for i in non_veg_tags]



meal_tags = []
for name in df['Name']:
    name_splitted = name.split()
    status = 'v'
    for word in name_splitted:
        if word.lower() in non_veg_tags:
            status = 'nv'
            
    if status == 'nv':
        meal_tags.append('Non Veg')
    else :
        meal_tags.append('Veg')
            
df['Type'] = meal_tags
df.insert(3, "Type", df.pop("Type"))

for i in range(len(df)):
    name_splitted = df.loc[i,'Name'].split()
    if ('Vegan' or 'vegan') in name_splitted:
        df.loc[i,'Type'] = 'Vegan'


# In[6]:


df.rename(columns={"Ratings out of 5": "Ratings 0.0-5.0", "Type": "Preference"},inplace=True)


# In[7]:


df['Ratings 0.0-5.0'] =  df['Ratings 0.0-5.0'].fillna(0)
df['Ratings count'] =  df['Ratings count'].fillna('0')


reviews_list = list(df['Reviews'].str.replace(r'[^\w\s]+', '',regex=True).values)

reviews_cleaned = []
for rev in reviews_list:
    if(pd.isna(rev)):
        reviews_cleaned.append(0)
    else:
        reviews_cleaned.append(int(rev.split(' ')[0]))
        
df['Reviews'] = reviews_cleaned



photos_list = list(df['Photos'].str.replace(r'[^\w\s]+', '',regex=True).values)

photos_cleaned = []
for pho in photos_list:
    if(pd.isna(pho)):
        photos_cleaned.append(0)
    else:
        photos_cleaned.append(int(pho.split(' ')[0]))
        
df['Photos'] = photos_cleaned




def get_cooking_time(cook_time):
    
    time = cook_time.split()
    if 'day' in time:
        index_d = time.index('day')
        n_day = time[index_d-1]
    else :
        n_day = 0
    
    if 'hrs' in time:
        index_h = time.index('hrs')
        n_hrs = time[index_h-1]
    else:
        n_hrs = 0
    
    if 'mins' in time:
        index_m = time.index('mins')
        n_mins = time[index_m-1]
    else:
        n_mins = 0
    
    time_in_mins = int(n_day) * 1440 +  int(n_hrs) * 60 +  int(n_mins)
    return time_in_mins



cooking_time_cleaned = []
for ct in df['Cooking time']:

    if(pd.isna(ct)):
        cooking_time_cleaned.append(np.nan)
    else:
        cooking_time_cleaned.append(get_cooking_time(ct))

df['Cooking time'] = cooking_time_cleaned


# In[8]:


df['Cooking time'] = df['Cooking time'].fillna(0)
df=df.dropna(subset=['Calories']).reset_index(drop=True)
df=df.dropna(subset=['Servings']).reset_index(drop=True)

df['Fats'] = df['Fats'].fillna('0g')
df=df.dropna(subset=['Carbs']).reset_index(drop=True)

df['Proteins'] = df['Proteins'].fillna('0g')
df['Sugars'] = df['Sugars'].fillna('0g')


columns_to_proceed = ['Name','URL','Category','Preference','Description','Ratings 0.0-5.0','Ratings count','Reviews',
                     'Photos','Cooking time','Calories','Servings','Ingredients','no of steps',
                      'Fats','Carbs','Sugars','Proteins',]

df = df[columns_to_proceed]


df['Ratings count'] = pd.to_numeric(df['Ratings count'].str.replace(r'[^\w\s]+', '',regex=True))


df['Fats'] = pd.to_numeric(df['Fats'].str.replace('g',''))
df['Carbs'] = pd.to_numeric(df['Carbs'].str.replace('g',''))
df['Proteins'] = pd.to_numeric(df['Proteins'].str.replace('g',''))
df['Sugars'] = pd.to_numeric(df['Sugars'].str.replace('g',''))


# In[9]:


#df.isnull().sum()


# # Exploring data

# In[10]:


#df['Category'].value_counts()


# In[11]:


#df.columns


# In[12]:


#df.sample(5)


# In[13]:


#df['Category'].value_counts()


# In[ ]:





# In[ ]:





# # Bar plots

# In[14]:


idf = df.interactive()


# In[15]:


radio_group_cat_type = pn.widgets.RadioButtonGroup(
    name='Radio Button Group', options=['Category','Preference'], button_type='default')

#radio_group_cat_type


# In[16]:


pipeline_cat_and_type = (idf[radio_group_cat_type].value_counts().sort_values(ascending=False)[0:12])


# In[17]:


#pipeline_cat_and_type


# In[18]:


cat_and_type_plot = pipeline_cat_and_type.hvplot(kind='barh',stacked=True, ylabel='count', xlabel='',
                          fontsize={
    'title': 15, 
    'labels': 14, 
    'xticks': 10, 
    'yticks': 10, 
})


# In[19]:


#cat_and_type_plot


# # Compare recipe macros

# In[20]:


rr = idf.groupby('Preference')[['Proteins','Fats','Carbs']].mean()

#rr


# In[21]:


macros_plot = rr.hvplot(stacked=False, rot=0,fontsize={
    'title': 15, 
    'labels': 14, 
    'xticks': 10, 
    'yticks': 10,},kind='barh', ylabel='value(gm)',xlabel='Preference')
#macros_plot


# # calories comparison

# In[22]:


calories_scatterplot_pipeline = (
    idf[['Preference','Proteins','Fats','Carbs','Calories']]
)


# In[23]:


yaxis_macros = pn.widgets.RadioButtonGroup(
    name='X axis', 
    options=['Proteins', 'Fats','Carbs'],
    button_type='default'
)


# In[24]:


calories_vs_macros_scatterplot = idf.hvplot(x=yaxis_macros, y='Calories', 
                                                                size=30,xlabel='value(gm)',
                                                                legend='top',
                                                                by='Preference',kind='scatter',
                                                         fontsize={
    'title': 15, 
    'labels': 14, 
    'xticks': 10, 
    'yticks': 10,
    'legend':10},hover_cols="Type")


# In[25]:


#calories_vs_macros_scatterplot


# In[26]:


import warnings
warnings.filterwarnings('ignore')


# In[ ]:





# # most famous dishes

# In[27]:


idf = df.interactive()


# In[28]:


idf = idf[idf['Ratings count']  > 10000].sort_values(['Ratings 0.0-5.0','Ratings count'],ascending=False)[0:5]


# In[29]:


yaxis_change = pn.widgets.RadioButtonGroup(
    name='X axis', 
    options=['Ratings 0.0-5.0','Ratings count','Reviews'],
    button_type='default'
)


# In[30]:


top_5_dishes = idf.hvplot(x='Name', y=yaxis_change, kind='scatter',size=100,
                  legend='top', rot=45, fontsize={
    'title': 15, 
    'labels': 14, 
    'xticks': 10, 
    'yticks': 10,
    'legend':10},xlabel='Recipe name')

#top_5_dishes


# In[31]:


#df.columns


# In[32]:


template = pn.template.FastListTemplate(
    title='Yumplatter, 28000+ Recipes, 26350 Ratings, 22 Categories', 
    sidebar_width = 300,
    sidebar=[pn.pane.Markdown("# Food Analysis"), 
             pn.pane.Markdown("#### ."), 
             pn.pane.PNG('wordcloud.png', sizing_mode='scale_both'),
             pn.pane.Markdown("## Settings")],
    main=[pn.Row(  pn.Column (  radio_group_cat_type,  cat_and_type_plot.panel(width=500,height=300)    )    , 
                 macros_plot.panel(width=500,height=330)), 
          pn.Row(  pn.Column (  yaxis_macros,  calories_vs_macros_scatterplot.panel(width=500,height=300)    )    , 
                 pn.Column (  yaxis_change,  top_5_dishes.panel(width=500,height=300)    )                       )   ],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
#template.show()
template.servable();


# In[ ]:





# In[ ]:





# In[ ]:




