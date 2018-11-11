
ip='0.0.0.0'
#ip='localhost'

port_db=7003
port_recommend=7004

# in minutes
period1=20

# in milliseconds
period2=$((20*60*1000))

python ./db/db_service.py ${ip} ${port_db} ${period1} &
sleep 5
python ./video_recommender/video_service.py ${ip} ${port_recommend} ${period2} &
