
kill_service_by() {

    PID_FILE=$1

    if [ -e ${PID_FILE} ]
    then
        PID1=`cat ${PID_FILE} | jq '.http'`
        PID2=`cat ${PID_FILE} | jq '.service'`
        PORT=`cat ${PID_FILE} | jq '.port'`

        #sudo kill `sudo lsof -t -i:${PORT}`

        if ps -p ${PID1} > /dev/null
        then
           kill -9 ${PID1}
           echo "Process with PID = {$PID1} is killed!"
        fi

        if ps -p ${PID2} > /dev/null
        then
           kill -9 ${PID2}
           echo "Process with PID = {$PID2} is killed!"
        fi

       rm ${PID_FILE}

    else
        case "$PID_FILE" in
        "pid_db_service.json")
            echo "HTTP service and DB service don't start before."
            ;;
        "pid_recommend_service.json")
            echo "HTTP service and video recommend service don't start before."
            ;;
        esac
    fi
}

kill_service_by pid_db_service.json
kill_service_by pid_recommend_service.json
