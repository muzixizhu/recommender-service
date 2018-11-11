
port1=7003
port2=7004
address=http://data-science-morelegends.westus2.cloudapp.azure.com
#address=http://localhost

#=======================================================================================================================
#curl ${address}:${port1}/api/users -XPOST -d '{"user": {"id": 1, "locale": "ru", "favorite_champion_ids": []}}'
#curl ${address}:${port1}/api/users/1 -XPATCH -d '{"user": {"locale": "en", "favorite_champion_ids": [100, 130]}}'
#curl ${address}:${port1}/api/users/1 -XDELETE

curl ${address}:${port1}/api/users -XPOST -d '{"user": {"id": 291926, "locale": "ru", "favorite_champion_ids": [140, 114, 61, 72, 119]}}'
curl ${address}:${port1}/api/users -XPOST -d '{"user": {"id": 291926, "locale": "ru", "favorite_champion_ids": [140, 114, 61, 72, 119]}}'


##=======================================================================================================================
#curl ${address}:${port1}/api/videos -XPOST -d '{"video": {"id": 1, "champion_ids": [100, 130, 216], "finders":
#["kda","early_summoner_death"], "roles": ["top", "jungle", "middle", "bottom", "support"],
#"champion_types": ["assassin", "fighter", "mage", "adc", "support", "tank"],
#"video_type": "roles/champions/mechanics", "locales": ["es", "ru", "pt", "zh_CN",
#"en"]}}'
#
#curl ${address}:${port1}/api/videos -XPOST -d '{"video": {"id": 2, "champion_ids": [777, 888, 111], "finders":
#["kda","early_summoner_death"], "roles": ["top", "jungle", "middle", "bottom", "support"],
#"champion_types": ["assassin", "fighter", "mage", "adc", "support", "tank"],
#"video_type": "roles/champions/mechanics", "locales": ["es", "ru", "pt", "zh_CN",
#"en"]}}'
#
#curl ${address}:${port1}/api/videos -XPOST -d '{"video": {"id": 1, "champion_ids": [], "finders":
#[], "roles": [],
#"champion_types": [],
#"video_type": null, "locales": ["es", "ru", "pt", "zh_CN",
#"en"]}}'
#
#curl ${address}:${port1}/api/videos -XPOST -d '{"video": {"id": 123, "champion_ids": [667], "finders":
#["kda","early_summoner_death"], "roles": ["top", "jungle", "middle", "bottom", "support"],
#"champion_types": ["assassin", "fighter", "mage", "adc", "support", "tank"],
#"video_type": "roles/champions/mechanics", "locales": ["es", "ru", "pt", "zh_CN",
#"en"]}}'
#
#
#curl ${address}:${port1}/api/videos/77 -XPATCH -d '{"video": {"champion_ids": [668, 888], "finders": ["kda",
#"early_summoner_death"], "roles": ["top", "jungle", "middle", "bottom", "support"],
#"champion_types": ["assassin", "fighter", "mage", "adc", "support", "tank"],
#"video_type": "roles/champions/mechanics", "locales": ["es", "ru", "pt", "zh_CN",
#"en"]}}'

#curl ${address}:${port1}/api/videos -XPOST -d '{"video": {"id":20000,"video_type":null,"roles":[],
#"champion_ids":[],"champion_types":[],"finders":[],"locales":["en","zh_CN","ru"]}}'


#=======================================================================================================================
curl "${address}:${port2}/api/videos/recommendations?locale=en&user_id=5157"
#curl "${address}:${port2}/api/videos/recommendations?locale=ru"
#curl "${address}:${port2}/api/videos/recommendations?locale=es"