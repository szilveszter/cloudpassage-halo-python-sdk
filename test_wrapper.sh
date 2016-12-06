#!/bin/sh

cd /source

BASE="py.test --cov=cloudpassage /source/tests/style /source/tests/unit"
INTEGRATION="py.test --cov=cloudpassage tests"
CODECLIMATE="codeclimate-test-reporter --file=/source/.coverage --debug"
SOURCE_CONFIG_TEMPLATE="/source/tests/configs/portal.yaml"
LOCAL_CONFIG_FILE="/source/tests/configs/portal.yaml.local"

# CodeClimate only records coverage for the default branch.  So if you have
# convigured the CODECLIMATE_REPO_TOKEN variable, we switch to the `master`
# branch before running tests and submitting results.

if [ ${CODECLIMATE_REPO_TOKEN} ]; then
  git checkout master
fi

if [ -z ${HALO_API_HOSTNAME} ]; then
  export HALO_API_HOSTNAME=api.cloudpassage.com
fi

if [ -z ${HALO_API_PORT} ]; then
  export HALO_API_PORT=443
fi

cat ${SOURCE_CONFIG_TEMPLATE} | envsubst > ${LOCAL_CONFIG_FILE}

# If HALO_API_KEY is not set, we assume that
# you're just doing style and unit tests.
# So we run those and exit.

if [ -z ${HALO_API_KEY} ]; then
  echo "Only running style and unit tests"
  ${BASE}
  exit $?
fi

# The first case falls through if you have HALO_API_KEY
# set, so we then run integration tests.

echo "Running style, unit, and integration tests"
${INTEGRATION}
RETCODE=$?
if [ ${RETCODE} != 0 ]; then
  exit ${RETCODE}
fi

# Finally, we use codeclimate-test-reporter to send in metrics.
if [ ${CODECLIMATE_REPO_TOKEN} ]; then
  ${CODECLIMATE}
fi

exit $?
