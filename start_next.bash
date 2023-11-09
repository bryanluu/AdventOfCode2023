#!/bin/bash
# This file starts the next or given day's challenge for the Advent of Code

advent_year=2022
programs=("clojure" "python" "node")
extensions=("clj" "py" "js")
cycle_count=${#programs[@]}

finish="finish_day.bash"
# if the previous day has already been finished
if [ -f $finish ]
then

  year=$(date +%Y)
  month=`date +%m`
  hour=`date +%H`
  # if the advent_year's challenges haven't been release yet
  if ([ $year == $advent_year ] && [ $month != 12 ] \
      && ( [ $month != 11 ] || [ $hour -lt 21 ] ) ) \
      || [ $(($year < $advent_year)) == 1 ] # Too early
  then
    echo "Advent of Code $advent_year hasn't started yet!"
  else

    today=`date +%d`
    days=`ls -d Day* | wc -l`
    # remove any leading zeroes
    days=${days#0}
    today=${today#0}
    hour=$(date +%H)
    # if the next day's challenge hasn't been released yet
    if [ $year == $advent_year ] && ([ $(($days > $today)) == 1 ] || ([ $today == $days ] && [ $(($hour < 21)) == 1 ]))
    then
      echo "Too early! Wait until December $(($days)) $advent_year"\
      ", 9pm PST for the next challenge."
    else
      # keep a table of time spent on each day
      timefile="times.csv"

      # cycle between programs each day
      day=$(( $days+1 ))
      i=$(( $day%$cycle_count ))
      prog=${programs[i]}
      ext=${extensions[i]}

      # handle inputs
      # if program is specified, use it
      # if specific day is specified, solve for that day
      force=""
      input_day=""
      input_prog=""
      while [ ! -z "$1" ]; do
        if [[ "$1" == "-p" ]] || [[ "$1" == "--program" ]]; then
          input_prog="$2"
          shift
          echo "Input program: $input_prog"
        elif [[ "$1" == "-f" ]] || [[ "$1" == "--force" ]]; then
          force="true"
        else
          input_day=$1
          echo "Input day: $input_day"
        fi
        shift
      done

      if [ -n "$input_prog" ]; then
        # use input_prog if it's one of the valid programs
        for ((i=0;i<$cycle_count;i++))
        do
          if [ "$input_prog" == "${programs[i]}" ]; then
            prog=$input_prog
            ext=${extensions[i]}
            break
          fi
        done
      fi

      skip=false
      # # set custom day if given and it is not yet finished
      if [[ $input_day =~ [0-9]+ ]] && [ $((1<=$input_day && $input_day<=25)) == 1 ];
      then
        if [ -f $timefile ]; then
          # Check if part 2 for the given day is not yet finished
          if [ $(egrep -c -e "^$input_day,(1\+)?2,.*$" $timefile) == 0 ]; then
            day=$input_day
          else
            echo "Day $input_day already completed..."
          fi
        else
          day=$input_day
        fi
      elif [ $(($day > 25)) == 1 ] && [ -z $input_day ]; then
        echo "Day required now..."
        unset progs_str
        for p in $programs
        do
          progs_str=$progs_str${progs_str:+|}$p
        done
        echo "Usage: . start_next.bash [-f|--force] [-p|--program $progs_str] day"
        skip=true
      elif [ -n "$input_day" ]; then
        echo "Invalid day given: $input_day"
      fi

      if [ -z "$force" ]; then
        read -p $"Work on Day $day using $prog? (y/n)"$'\n' reply
        [[ $reply =~ ^[Yy].*$ ]] || skip=true # skip if reply is No
        [ $skip == true ] && echo "Stopping..."
      fi

      if [ $skip == false ]; then

        echo "Working on Day $day using $prog..."
        padded_day=$((( $day < 10 )) && echo "0")$day
        dir="Day$padded_day"
        codefile="Day$padded_day.$ext"

        mkdir -p $dir
        mv $finish $dir

        [ ! -f "$dir/$codefile" ] && cp "Templates/${prog}_template.$ext" \
            "$dir/$codefile" # Copy template if the file doesn't exist
        # cd $dir

        date > "$dir/start"

        echo "Run '$dir/finish_day.bash [-a OR --all]' to complete solution."

        tester="$dir/run.bash"
        echo '#!/bin/bash' > "$tester"
        echo "$prog $codefile" '$@' >> "$tester"
        chmod +x "$tester"

        subl "$dir/$codefile" # start editing

      fi

    fi

  fi

else

  unfinished=`dirname */$finish`
  day=${unfinished//[!0-9]/}
  tester="$unfinished/run.bash"
  dir=$unfinished
  echo "Cannot start until Day $day is completed!"
  echo "Run '$tester [filename]' to test program..."
  echo "Run '$dir/finish_day.bash [-a OR --all]' in '$unfinished/' to finish first..."

fi
