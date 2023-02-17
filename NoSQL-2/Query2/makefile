run:
	date +%s > _time_$@.txt
	(cat access_log11.txt | python mapper.py | python combiner.py & cat access_log12.txt | python mapper.py | python combiner.py) | python reducer.py > result.txt
	echo $$(($$(date +%s)-$$(cat  _time_$@.txt)))