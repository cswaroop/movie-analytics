function hit_movie(s)
	local function mapper(rec)
		local k = rec['productId']
		return map { [k] = 1 }
	end

	local function merger(val1, val2)
		return val1 + val2
		end

	local function reducer(m1, m2)
		return map.merge(m1, m2, merger)
	end

	return s : map(mapper) : reduce(reducer)

end

function active_user(s)
	local function mapper(rec)
		local k = rec['profName']
		return map { [k] = 1 }
	end

	local function merger(val1, val2)
		return val1 + val2
		end

	local function reducer(m1, m2)
		return map.merge(m1, m2, merger)
	end

	return s : map(mapper) : reduce(reducer)
end

function avg_rating(s, movie_name)
	local function mapper(rec)
		if rec['rating'] and rec['productId'] == movie_name then
			return map {
				value =  tonumber(rec['rating']),
				count =  1,
				}
		else
			return map {
				value =  0,
				count =  0,
				}
		end
	end
	local function reducer(m1, m2)
		return map {
				value = m1['value'] + m2['value'],
				count = m1['count'] + m2['count'],
			}
	end
	local function div(m)
		if m['value'] ~= 0 then
			return m['value'] / m['count']
		else
			return 0
		end
	end
	return s : map(mapper) : reduce(reducer) : map(div)
end

function most_useful(s, min)
	local function mapper(rec)
		local ll = list()
		local k = tonumber(rec['helpfullness'])
		if k > tonumber(min) then
			list.append(ll, rec['productId'])
		end
		return ll
	end

	local function reducer(m1, m2)
		return list.merge(m1, m2)
	end

	return s : map(mapper) : reduce(reducer)
end
