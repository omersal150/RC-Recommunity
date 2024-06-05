{{/*
Expand the name of the chart.
*/}}
{{- define "rc-recommunity-helm.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "rc-recommunity-helm.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "rc-recommunity-helm.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "rc-recommunity-helm.labels" -}}
helm.sh/chart: {{ include "rc-recommunity-helm.chart" . }}
{{ include "rc-recommunity-helm.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "rc-recommunity-helm.selectorLabels" -}}
app.kubernetes.io/name: {{ include "rc-recommunity-helm.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Helper function to check if HorizontalPodAutoscaler CRD is available
*/}}
{{- define "rc-recommunity-helm.hasHPACRD" -}}
{{- $hpaCRD := "horizontalpodautoscalers.autoscaling" -}}
{{- $hasCRD := false -}}
{{- range .CRDs -}}
  {{- if eq .Name $hpaCRD -}}
    {{- $hasCRD = true -}}
  {{- end -}}
{{- end -}}
{{- $hasCRD -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "rc-recommunity-helm.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "rc-recommunity-helm.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
