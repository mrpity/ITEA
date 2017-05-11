node {
   
   stage "STAGE 1. Chechout"
   //git git@bitbucket.org:whirlsoftware/whirl_ansible.git
   git branch: 'master',  url: 'git@bitbucket.org:whirlsoftware/whirl_ansible.git'
   
   stage "STAGE 2. Print"
   echo "Prigt Stage 1"
   
   stage "STAGE 3. Print envs variables"
   echo "JAVA_HOME: ${env.JAVA_HOME}"
   echo "JAVA_HOME: ${env}"
}
