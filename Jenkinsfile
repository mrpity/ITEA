node {
   
   stage "STAGE 1. Chechout"
   //git git@bitbucket.org:whirlsoftware/whirl_ansible.git
   git branch: 'master',  url: 'git@bitbucket.org:whirlsoftware/whirl_ansible.git'
   
   stage "STAGE 2. Print"
   echo "Prigt Stage 1"
   
   stage "STAGE 3. Print envs variables"
   echo "JAVA_HOME: ${env.JAVA_HOME}"
   echo "My test: ${env.TEST_VAR}"
   def TVAR = 'atatata'
   echo "variable: ${TVAR}"
   
   stage "STAGE 4. DSL JOB create"
   jobDsl scriptText: 
   '''
 
   job(\'Dima_pipeline\') {
    description(\'Dima_pipeline\')
    concurrentBuild()
    wrappers {
        colorizeOutput()
        timestamps()
        buildName(\'test\')
    }
    steps {
       shell(\'echo "success"\')
    }
   }
   '''
   stage "STAGE 5. DSL JOB run"
   build 'Dima_pipeline'
   
   stage "STAGE 6"
   def branches = [:]

   for (int i = 0; i < 4; i++) {
      def index = i //if we tried to use i below, it would equal 4 in each job execution.
      branches["branch${i}"] = "atata-${i}"
   }
   echo branches
   echo ${branches}
}
