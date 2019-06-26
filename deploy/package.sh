#!/usr/bin/env bash
REGION=${1:-us-west-2}
# staging path
TMP_PATH='/tmp'
# dir in staging path
TMP_DIR=`date +%Y/%m/%d`
# path to pip code to
CODE_PATH="${TMP_PATH}/${TMP_DIR}/code"
# name of the zip package
ZIP_NAME=`date +%Y-%m-%d_%H.%M.%S.zip`
# path to the lambda module
API_PATH='./src'
HANDLERS=(api_handler.py sqs_handler.py)
CWD=$(pwd)

# Update to match stack/resource names
FUNC_NAME="Mtaws"
CODE_BUCKET_NAME="apicode"

# gather funcs to update. Must contain JumpCloud
FUNCS=$(aws lambda list-functions --query 'Functions[].FunctionName' --output text --region ${REGION})
FUNCS=($FUNCS)

TO_UPDATE=()

for f in ${FUNCS[*]}
do
    if  [[ $f == *"${FUNC_NAME}"* ]]; then
        TO_UPDATE+=(${f})
    fi
done

# get the lambda code bucket
BUCKETS=$(aws s3api list-buckets --query "Buckets[].Name"  --output text --region ${REGION})
BUCKETS=($BUCKETS)

for b in ${BUCKETS[*]}
do
    if [[ $b == *"${CODE_BUCKET_NAME}"* ]]; then
        CODE_BUCKET=$b
    fi
done

# do we have functions to update?
NUM_FUNCS=${#TO_UPDATE[@]}

if [ $NUM_FUNCS -eq 0 ]; then
    echo "NO FUNCS TO UPDATE"
    exit 1
fi

# ensure and clean staging dirs
mkdir -p "${TMP_PATH}/${TMP_DIR}"
rm -rf ${CODE_PATH}
mkdir -p ${CODE_PATH}

# INSTALL TO STAGING DIR
docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):$(pwd) -w $(pwd) -v /tmp:/tmp python:3.6  pip install -r ${API_PATH}/requirements.txt -t ${CODE_PATH}

# COPY LAMBDA CODE/MODULE TO STAGING PATH
cp -r ${API_PATH}/* ${CODE_PATH}

# MOVE HANDLERS TO ROOT DIRECTORY
for h in ${HANDLERS[*]}
do
    mv ${CODE_PATH}/mtaws/${h} ${CODE_PATH}/${h}
done


echo "ZIPPING CODE"
# ZIP CODE
cd ${CODE_PATH}
zip -r ${TMP_PATH}/${TMP_DIR}/$ZIP_NAME ./* --exclude=*env/*

# go back to origin working dir
cd ${CWD}

echo "UPLOADING TO S3: ${CODE_BUCKET}"
# STAGE ON S3
aws s3 cp ${TMP_PATH}/${TMP_DIR}/$ZIP_NAME s3://${CODE_BUCKET}/${TMP_DIR}/${ZIP_NAME} --region ${REGION}

for f in ${TO_UPDATE[*]}
do
    echo "UPDATING FUNC: ${f}"
    aws lambda update-function-code --function-name ${f} --s3-bucket ${CODE_BUCKET} --s3-key ${TMP_DIR}/${ZIP_NAME} --region ${REGION}
done
