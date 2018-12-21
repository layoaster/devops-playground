# Devops Playground

[![pipeline status](https://gitlab.com/audiadis/devops-playground/badges/develop/pipeline.svg)](https://gitlab.com/audiadis/devops-playground/commits/develop) [![coverage report](https://gitlab.com/audiadis/devops-playground/badges/develop/coverage.svg)](https://gitlab.com/audiadis/devops-playground/commits/develop)

Project to test the integration between Gitlab and GCP/Kubernetes. It also
serves to define a basic skeleton for microservices-based projects that can
be deployed to a Kubernetes cluster in Google Cloud and that developers can get
up & running locally with a docker-compose.


## Architecture

The application follows a microservices architecture. It basically consist of
two microservices:

* Web Aplication (RESTful API).
* Database (Redis).


## Application

The web application is a RESTful API with a single endpoint (`/`) that only
support the `GET` method.

It basically returns a JSON response with the number of times the endpoint
has been hit:

```Json
{
    "Hello-World! hits": 3
}
```

## Development tools

The project is configured for the following tools:

* `Pytest` for unittesting and coverage.
* `flake8` for code style/quality enforcement and *PEP-8* linting.


## Infrastructure

### Local Deployment

To run/deploy de application locally (developer's machine) the projects uses
`docker-compose` so a simple `docker-compose up` is enough to test/debug the
app.

### Cloud Deployment

The application is designed to be deployed in Cloud-based solutions with
**Kubernetes** (with Google Cloud Container Engine in mind). To simplyfy and
ease the deployment `Helm` is used.


On this particular project two Helm Charts are being used:

1. An *external* chart (`stable/redis`) to deploy Redis.
2. A manually created chart to deplopy the RESTful API web application.

**Cluster configuration**

The cluster should be provisioned with the following components to get a
 fully functional deployment:

  * The Helm server
    ([Tiller](https://docs.helm.sh/using_helm/#installing-tiller))
    with RBAC-enabled config to deploy charts.
  * The `ingress-nginx` controller
    ([link](https://github.com/kubernetes/ingress-nginx)) to expose the application
    with a L7 Load Balancer.
  * The ([`cert-manager`](https://github.com/jetstack/cert-manager)) to
    automatically provision and manage TLS certificates from *Let's Encrypt*.
  * A Cluster with at least read access to Google Cloud Storage (GKE only).

### CI/CD

The project uses the [Gitlab CI/CD](https://docs.gitlab.com/ee/ci/README.html)
capabilities to build,test and deploy the application.

The project CI/CD pipeline has the following stages:

* `build`: build the docker images.
* `test`: run application unitest's suite and checks the code quality.
* `review`: temporary branch-based deployment.
* `staging`: deployment to the staging cluster/environment.
* `production`: deployment to the production cluster/environment.

The project's folder `etc` contains everything that our pipeline will need. It's structured in the following way:

```
etc
├── cd                                  <-- Deployment stages
│   └── helm-charts                     <-- Helm charts
│       ├── myapp                       <-- Custom app chart
│       │   ├── Chart.yaml
│       │   ├── templates
│       │   │   ├── deployment.yaml
│       │   │   └── ....
│       │   ├── ... 
│       │   └── values.yaml
│       └── redis                       <-- Not really a chart but the values for
│           └── staging-values.yaml         an external chart and environment.
└── ci                                  <-- Build/Test stages
    └── docker-compose-ci.yml           <-- docker-compose config for building and
                                            running test
```


## Devops tools

* [Google Cloud SDK](https://cloud.google.com/sdk/docs/downloads-interactive)
  (kubectl is included).
* [Helm client](https://docs.helm.sh/using_helm/#installing-the-helm-client).
* [kubectx](https://github.com/ahmetb/kubectx)


## Useful links

* Gitlab CI/CD [reference](https://docs.gitlab.com/ee/ci/README.html).
* Gitlab CI/CD [variables](https://docs.gitlab.com/ee/ci/variables/README.html).
* Gitlab Auto-devops CI/CD
  [template](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/lib/gitlab/ci/templates/Auto-DevOps.gitlab-ci.yml).
* Gitlab CI/CD pipelines [examples](https://gitlab.com/gitlab-examples).
* Helm [documentation](https://docs.helm.sh/).
* Helm/Tiller required
  [config](https://docs.gitlab.com/ee/install/kubernetes/preparation/tiller.html#preparing-for-helm-with-rbac)
  for RBAC-enabled clusters.
* Helm Charts template developer's
  [guide](https://docs.helm.sh/chart_template_guide/).
* Nginx ingress controller
  [live docs](https://kubernetes.github.io/ingress-nginx/).
* Cert-manager
  [documentation](https://cert-manager.readthedocs.io/en/latest/index.html).
* Cert-manager
  [tutorial](https://github.com/jetstack/cert-manager/blob/master/docs/tutorials/quick-start/index.rst)
  for *nginx-ingress* and *Let's Encrypt*.

