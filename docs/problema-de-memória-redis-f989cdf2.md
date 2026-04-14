<!-- title: Problema de memória Redis | url: https://outline.seazone.com.br/doc/problema-de-memoria-redis-LMb33AOcIG | area: Tecnologia -->

# Problema de memória Redis

Tags: AWS, Redis

<https://medium.com/@akhshyganesh/redis-enabling-memory-overcommit-is-a-crucial-configuration-68dbb77dae5f>

<https://redis.io/docs/latest/operate/oss_and_stack/management/admin/>

**terminal log (docker logs <container_id>)** → 1:M 03 May 2024 14:41:53.749 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can can also cause failures without low memory condition, see <https://github.com/jemalloc/jemalloc/issues/1328>. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.

### Update

Para resolver esse problema de vez, tivemos que de fato aumentar o disco da máquina que roda o Redis+OpenSearch (stg-reservas-001).

Para isso, seguimos esses passos: [Aumentar volume vinculado à uma EC2](/doc/aumentar-volume-vinculado-a-uma-ec2-JCw2OLRW8m)