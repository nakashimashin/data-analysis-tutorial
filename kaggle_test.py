import kaggle

competitions = kaggle.api.competitions_list(search='titanic')

for competition in competitions:
    print(f"ID: {competition.ref}, Title: {competition.title}")