<!-- title: Queda do job Sagemaker blockDetection | url: https://outline.seazone.com.br/doc/queda-do-job-sagemaker-blockdetection-KEUfOc9oof | area: Tecnologia -->

# Queda do job Sagemaker blockDetection

No dia 15/09/2025 o pipeline do Sagemaker BlockDetectionNNSPipelineProd teve falha de execução. Inicialmente foi feito uma análise comparativa dos logs da execução bem sucedida e da que falhou e foi descoberto que teve uma mudança do ambiente de execução com um downgrade da versão do Python (3.9 para 3.8) para as bibliotecas scikit-learn e pandas. 


Na investigação, encontrei que isso já é um bug conhecido <https://github.com/aws/sagemaker-scikit-learn-container/issues/249> e que a AWS necessita fazer um novo release da imagem para corrigir esse bug.


Como medida paliativa, foi realizado a implementação de uma imagem customizada para rodar os jobs no container ao invés da imagem da AWS. A imagem foi registrada no ECR e depois incorporada ao código-fonte  do notebook de create_pipeline.ipynb no Sagemaker AI Studio. 


Além disso, ao realizar a nova execução, a instância que rodava a parte do pipeline com os dados do Lake estourou a memória, então tive que aumentar o tamanho da instância no código do notebook para fazer funcionar.