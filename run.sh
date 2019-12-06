#!/bin/bash
# author: wct fxy
check()
{
    if (($(ps aux|grep app.py|grep -v grep|wc -l) == 0));then
        # stopped
        return 1;
    else
        # running
        return 0;
    fi
}

start()
{
    check
    if (($? == 1));then
        echo -n 'app.py to start......'
        path=$(dirname $0)
        if [[ $path != '.' ]];then
            cd $path
        fi
        nohup /home/seemmo/share/python/centos/python3.6.6/bin/python3 app.py --debug=0 --port=9000 >nohup.out 2>&1 &
        # nohup python3 app.py --debug=0 --port=9000 >nohup.out 2>&1 &
        while true
        do
            check
            if (($? == 1));then
                echo -n '...'
                sleep 1
            else
                echo -e '\033[32mstarted\033[1m\033[0m'
                break
            fi
        done
    else
        echo "app.py has been running!!!"
    fi
}

fstop()
{
    check
    if (($? == 1));then
        echo "app.py has been stopped!!!"
    else
        echo -n 'app.py force to stop.....'
        ps aux|grep app.py|grep -v grep|awk '{print $2}'|xargs kill -9
        while true
        do
            check
            if (($? == 1));then
                echo -e '\033[32mstopped\033[1m\033[0m'
                break
            else
                echo -n '...'
                sleep 1
            fi
        done
    fi
}

stop()
{
    check
    if (($? == 1));then
        echo "app.py has been stopped!!!"
    else
        echo -n 'app.py to stop.....'
        spid=1
        tp_list=($(ps aux|grep app.py|grep -v grep|awk '{print $2}'|xargs))
        for tpid in ${tp_list[@]}
        do
            if ((spid == 1));then
                spid=$tpid
            elif ((tpid < spid));then
                spid=$tpid
            fi
        done
        kill -15 $spid
        retry_time=3
        while true
        do
            if ((retry_time == 0));then
                echo
                fstop
                break
            fi
            check
            if (($? == 1));then
                echo -e '\033[32mstopped\033[1m\033[0m'
                break
            else
                ((retry_time=retry_time-1))
                echo -n '.'
                sleep 1
            fi
        done
    fi
}

status()
{
    check
    if (($? == 1));then
        echo -e 'app.py now is \033[32mstopped\033[1m\033[0m'
    else
        echo -e 'app.py now is \033[32mrunning\033[1m\033[0m'
    fi
}

restart() {
    check
    if (($? == 1));then
        start
    else
        stop
        while true
        do
            check
            if (($? == 1));then
                start
                break
            else
                sleep 1
            fi
        done
    fi
}

if (($# == 1));then
    case $1 in
        start|stop|status|restart|fstop)
            $1
            ;;
        *)
            echo "Usage: bash $0 {start|stop|status|restart|fstop}"
            exit 2
    esac
else
    echo "Usage: bash $0 {start|stop|status|restart|fstop}"
    exit 2
fi
