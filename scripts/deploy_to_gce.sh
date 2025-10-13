#!/usr/bin/env bash
set -euo pipefail

# Deploy the US College Admission Counseling stack to a Google Compute Engine
# instance backed by the Container-Optimized OS image. The script assumes you
# have already authenticated with `gcloud auth login` and selected a project.

PROJECT_ID="${PROJECT_ID:-}"
REGION="${REGION:-us-central1}"
ZONE="${ZONE:-us-central1-a}"
ARTIFACT_REPO_NAME="${ARTIFACT_REPO_NAME:-us-college-counseling}"
IMAGE_NAME="${IMAGE_NAME:-us-college-counseling}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
INSTANCE_NAME="${INSTANCE_NAME:-us-college-counseling}"
MACHINE_TYPE="${MACHINE_TYPE:-e2-standard-2}"
ENV_FILE="${ENV_FILE:-backend/.env.docker}"

if [[ -z "${PROJECT_ID}" ]]; then
  echo "PROJECT_ID is required. Set it in the environment or export PROJECT_ID before running." >&2
  exit 1
fi

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "Environment file '${ENV_FILE}' not found. Provide a Docker-ready env file via ENV_FILE." >&2
  exit 1
fi

set -x

gcloud config set project "${PROJECT_ID}"

REPO_PATH="${REGION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REPO_NAME}"

if ! gcloud artifacts repositories describe "${ARTIFACT_REPO_NAME}" \
  --location="${REGION}" >/dev/null 2>&1; then
  gcloud artifacts repositories create "${ARTIFACT_REPO_NAME}" \
    --repository-format=docker \
    --location="${REGION}" \
    --description="Container images for the US college counseling platform"
fi

gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet

docker build -t "${REPO_PATH}/${IMAGE_NAME}:${IMAGE_TAG}" .

docker push "${REPO_PATH}/${IMAGE_NAME}:${IMAGE_TAG}"

if ! gcloud compute firewall-rules describe "${INSTANCE_NAME}-allow-http" >/dev/null 2>&1; then
  gcloud compute firewall-rules create "${INSTANCE_NAME}-allow-http" \
    --allow=tcp:80,tcp:8000 \
    --target-tags="${INSTANCE_NAME}" \
    --description="Allow HTTP traffic to the counseling app"
fi

if gcloud compute instances describe "${INSTANCE_NAME}" --zone="${ZONE}" >/dev/null 2>&1; then
  gcloud compute instances delete "${INSTANCE_NAME}" --zone="${ZONE}" --quiet
fi

gcloud compute instances create-with-container "${INSTANCE_NAME}" \
  --zone="${ZONE}" \
  --machine-type="${MACHINE_TYPE}" \
  --tags="${INSTANCE_NAME}" \
  --container-image="${REPO_PATH}/${IMAGE_NAME}:${IMAGE_TAG}" \
  --container-env-file="${ENV_FILE}" \
  --boot-disk-size=30GB \
  --boot-disk-type=pd-balanced \
  --scopes=https://www.googleapis.com/auth/cloud-platform

set +x

echo "Deployment complete. Once the VM finishes booting, access the app via the instance's external IP on port 8000."
