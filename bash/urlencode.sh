#!/bin/bash

# echo "total args: $#"

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <url>"
    exit 1
fi

url=$*

echo "Full url: $url"

echo "${url:0:4}"

# verify it is a url string
if [[ ${url:0:4} != "http" ]]; then
    echo "Invalid url, must start with http"
    exit 1
fi

# encode url
for ((i=0; i<${#url}; i++)); do
    char="${url:i:1}"
    
    dec=$(printf "%d" "'$char")
    hex=$(printf "%x" "'$char")

    if [[ dec -eq 43 || dec -eq 32 ]]; then
    	echo "space or +: ${char}"

	url=${url/${char}/%'${hex}}
    elif [[ dec -gt 32 && dec -lt 126 ]]; then
    	echo "utf8: ${char}"
    else
	echo "encode: ${char}"

	url=${url/${char}/%${hex}}
    fi
done

printf "\n"

url=${url/ /%20}

echo "final url: ${url}"
