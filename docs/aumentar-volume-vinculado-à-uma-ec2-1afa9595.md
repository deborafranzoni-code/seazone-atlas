<!-- title: Aumentar volume vinculado à uma EC2 | url: https://outline.seazone.com.br/doc/aumentar-volume-vinculado-a-uma-ec2-KIlcKOeRkO | area: Tecnologia -->

# Aumentar volume vinculado à uma EC2

Tags: AWS, EC2, EC2 Volume

Siga as instruções aqui nessa documentação da AWS:

[Extend the file system after resizing an EBS volume - Amazon EBS](https://docs.aws.amazon.com/ebs/latest/userguide/recognize-expanded-volume-linux.html?icmpid=docs_ec2_console)

### Resumo (leia a doc da aws antes)

* Criar Snapshot
* Aumentar volume
* Aguardar o "Volume state" ficar com status **"✅ In-use"**
* Acessar máquina via SSH
* Rodar os comandos:
  * lsblk: Veja que continua o mesmo tamanho anterior
  * df -h: Veja que o disco já está com o tamanho novo porém a partição ainda está menor.
* Extenda o tamanho do volume:
  * `sudo growpart /dev/nvme0n1 1`
  * `lsblk`: veja que o volume já está com o novo tamanho
  * `df -hT`: Veja que a partição ainda está no tamanho antigo
  * `sudo xfs_growfs -d /`
  * `df -hT`: Veja que a partição já está com o novo tamanho
  * Fim 😁