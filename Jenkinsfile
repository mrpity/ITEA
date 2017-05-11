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
   
   stage "STAGE 4. DSL JOB create 1"
   jobDsl scriptText: 
   '''
 
   job(\'Dima_pipeline1\') {
    description(\'Dima_pipeline1\')
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
      stage "STAGE 5. DSL JOB create 2"
   jobDsl scriptText: 
   '''
 
   job(\'Dima_pipeline2\') {
    description(\'Dima_pipeline2\')
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
   
  // stage "STAGE 5. DSL JOB run"
   //build 'Dima_pipeline'
   
   stage "STAGE 6"
   def branches = [:]

   for (int i = 0; i < 2; i++) {
      def index = i 
      branches["branch${i}"] = 'build "Dima_pipeline${i}"'
    }
   echo "${branches}"
   parallel branches
   
   
}
