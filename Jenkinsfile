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
   
   stage "STAGE 4. DSL JOB"
   jobDsl scriptText: 
   '''
   // Set name\'s for MultiPhase jobs
   def CMS_DEPLOY_manual = \'CMS_DEPLOY_ansible\'
   def CDS_DEPLOY_manual = \'CDS_DEPLOY_ansible\'
   def WAS_DEPLOY_manual = \'WAS_DEPLOY_ansible\'
   def RTA_DEPLOY_manual = \'RTA_DEPLOY_ansible\'
   def OLA_DEPLOY_manual = \'OLA_DEPLOY_ansible\'

   // Get env vars from current build
   def thr = Thread.currentThread()
   def build = thr?.executable
   def envVarsMap = build.parent.builds[0].properties.get("envVars")
   
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
   
}
