#!/bin/bash
# Usage ./test-dns.sh $zone_file $domain_name $name_server

zone_file=$1

domain=$2

name_server=$3

[ $# -eq 0 ] && { echo "Usage: $0 zone_file domain_name name_server"; exit 1; }

# Define an array to hold the subdomains
subdomains=()

# Define an array to hold the responses from the dig command
responses=()

# Define an array to hold the target values
target_values=()

# Loop through the file microguide.zone
while read line; do
  # Get the start of the line up to the first space
  subdomain=$(echo $line | cut -d ' ' -f1)

  # Add the subdomain to the array
  subdomains+=("$subdomain")

  # Get the last word of the line and add it to the target_values array
  target_value=$(echo $line | rev | cut -d ' ' -f1 | rev | awk '{print tolower($0)}')
  target_values+=("$target_value")
done < $1

for subdomain in "${subdomains[@]}"; do
 # Run a dig command for each subdomain with the +short option and add the response to the responses array
  response=$(dig +short $subdomain.$2 @$3)
  responses+=("$response")
done

iterator=0
# Loop through the array of responses
for response in "${responses[@]}"; do
  # Compare the response to each element of the target_values array
  if [ "$response" == "${target_values[$iterator]}" ]; then
    echo "Matching response: $response"
  else
     echo "Non-matching response: $response"
   fi
  let "iterator++"
done