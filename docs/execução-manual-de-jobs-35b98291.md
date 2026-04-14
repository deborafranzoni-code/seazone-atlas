<!-- title: Execução Manual de Jobs | url: https://outline.seazone.com.br/doc/execucao-manual-de-jobs-dXEvhSfBl8 | area: Tecnologia -->

# Execução Manual de Jobs

# 📄 Execução Manual de Jobs no GCP (Cloud Run)



---

## 1️⃣ Job: `airbnb-image-job-prd`

### a) Atualizar e executar **Refiller**

```bash
gcloud run jobs update airbnb-image-job-prd \
  --project data-resources-448418 \
  --image us-central1-docker.pkg.dev/data-resources-448418/airbnb-image-scraper-repo/airbnb-image-scraper:latest \
  --region us-central1 \
  --set-env-vars=GOOGLE_CLOUD_PROJECT=data-resources-448418 \
  --set-env-vars=GOOGLE_APPLICATION_CREDENTIALS=./sandbox-439302-e5ebce15d501.json \
  --set-env-vars=USER_AGENTS_BUCKET=scrapers-test \
  --set-env-vars=AIRBNB_SCRAPERS_USER_AGENTS_KEY=pipe-essential-files/user-agents/mesh-user-agents.json \
  --args="refiller,--topic=image-metadata-input,--gcs_directory=ids_refiller/"

gcloud run jobs execute airbnb-image-job-prd --region us-central1
```


---

### b) Atualizar e executar **Image Metadata**

```bash
gcloud run jobs update airbnb-image-job-prd \
  --project data-resources-448418 \
  --image us-central1-docker.pkg.dev/data-resources-448418/airbnb-image-scraper-repo/airbnb-image-scraper:latest \
  --region us-central1 \
  --tasks=80 \
  --parallelism=80 \
  --task-timeout=1800s \
  --set-env-vars=GOOGLE_CLOUD_PROJECT=data-resources-448418 \
  --set-env-vars=GOOGLE_APPLICATION_CREDENTIALS=./sandbox-439302-e5ebce15d501.json \
  --set-env-vars=USER_AGENTS_BUCKET=categorizacao_pipeline \
  --set-env-vars=AIRBNB_SCRAPERS_USER_AGENTS_KEY=pipe-essential-files/user-agents/mesh-user-agents.json \
  --args="image_metadata"

gcloud run jobs execute airbnb-image-job-prd --region us-central1 --project data-resources-448418
```


---

### c) Atualizar e executar **Images**

```bash
gcloud run jobs update airbnb-image-job-prd \
  --image us-central1-docker.pkg.dev/data-resources-448418/airbnb-image-scraper-repo/airbnb-image-scraper:latest \
  --region us-central1 \
  --tasks=80 \
  --parallelism=80 \
  --task-timeout=14400s \
  --set-env-vars=GOOGLE_CLOUD_PROJECT=data-resources-448418 \
  --set-env-vars=GOOGLE_APPLICATION_CREDENTIALS=./sandbox-439302-e5ebce15d501.json \
  --set-env-vars=USER_AGENTS_BUCKET=categorizacao_pipeline \
  --set-env-vars=AIRBNB_SCRAPERS_USER_AGENTS_KEY=pipe-essential-files/user-agents/mesh-user-agents.json \
  --args="images"

gcloud run jobs execute airbnb-image-job-prd --region us-central1
```


---

## 2️⃣ Job: `gemini-image-score-job`

### a) Atualizar e executar

```bash
gcloud run jobs update gemini-image-score-job \
  --project data-resources-448418 \
  --region us-central1 \
  --image us-central1-docker.pkg.dev/data-resources-448418/gemini-pipeline-repo/image-score-pipeline:latest \
  --task-timeout=5h

gcloud run jobs execute gemini-image-score-job \
  --region us-central1 \
  --wait
```

### b) Atualizar para nova versão da imagem (opcional)

```bash
gcloud run jobs update gemini-image-score-job \
  --image=us-central1-docker.pkg.dev/data-resources-448418/gemini-pipeline-repo/image-score-pipeline:latest \
  --region=us-central1

gcloud run jobs execute gemini-image-score-job \
  --region=us-central1 \
  --wait
```


---

## 3️⃣ Job: `image-score-classifier-job`

### a) Atualizar e executar

```bash
gcloud run jobs update image-score-classifier-job \
  --image=us-central1-docker.pkg.dev/data-resources-448418/classifier-pipeline-repo/image-score-classifier:latest \
  --region=us-central1

gcloud run jobs execute image-score-classifier-job \
  --region us-central1 \
  --wait
```


---