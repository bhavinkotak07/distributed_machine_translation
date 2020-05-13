import sys
if __name__ == "__main__":
    name = sys.argv[1]
    instances = sys.argv[2]
    fname = name + '.yaml'
    confg = '''apiVersion: apps/v1
kind: Deployment
metadata: 
  labels: 
    app.kubernetes.io/name: ''' + name +'''
  name: '''+name+'''
spec: 
  replicas: ''' + instances + '''
  selector: 
    matchLabels: 
      app.kubernetes.io/name: ''' + name + '''
  template: 
    metadata: 
      labels: 
        app.kubernetes.io/name: ''' + name + '''
    spec: 
      containers: 
        - 
          command: ["bash","index.sh"]
          image: mt2
          imagePullPolicy: IfNotPresent
          name: '''+name+'''
          ports: 
            - 
              containerPort: 8080
          resources: 
            limits: 
              memory: 2Gi
            requests: 
              memory: 600Mi
          volumeMounts: 
            - 
              mountPath: /host/uploads/''' + name + '''
              name: code
          workingDir: /host/uploads/'''+name + '''
      volumes: 
        - 
          hostPath: 
            path: /host/uploads/''' + name + '''
          name: code


    '''

    with open(fname, 'w') as f:
        f.write(confg)
