
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.24.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.7.1"
    }
  }
}

data "archive_file" "greeting_agent" {
  type        = "tar.gz"
  output_path = "${path.module}/greeting_agent.tar.gz"
  source_dir  = "${path.module}/../greeting_agent"

  excludes = [
    ".git/**",
    ".gitignore",
    ".env",
    "__pycache__/**",
    "*.pyc"
  ]
}

resource "google_vertex_ai_reasoning_engine" "this" {
  display_name = "greeting-agent"
  description  = "A greeting agent"
  region       = "us-central1"
  project      = "<PROJECT_ID>"

  spec {
    agent_framework = "google-adk"
    # class_methods = jsonencode(
    #   [
    #     {
    #       api_mode = "stream"
    #       name     = "stream_query"
    #       parameters = {
    #         type = "object"
    #         required = [
    #           "user_id",
    #           "session_id",
    #           "message"
    #         ]
    #         properties = {
    #           user_id    = { "type" : "string" }
    #           session_id = { "type" : "string" }
    #           message    = { "type" : "string" }
    #         }
    #       }
    #     }
    #   ]
    # )
    source_code_spec {
      inline_source {
        source_archive = filebase64("${path.module}/greeting_agent.tar.gz")
      }

      python_spec {
        entrypoint_module = "agent"
        entrypoint_object = "app"
        requirements_file = "requirements.txt"
        version           = "3.11"
      }
    }
  }
}
