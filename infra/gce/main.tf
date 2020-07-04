provider "google" {
 project     = "tldr-278619"
 region      = "us-central1"
}

resource "google_compute_instance" "summarizer" {
 name         = "summarizer"
 machine_type = "e2-standard-2"
 zone         = "us-central1-a"
 can_ip_forward       = false

 scheduling {
   automatic_restart   = true
   on_host_maintenance = "MIGRATE"
 }

 boot_disk {
   initialize_params {
     image = "cos-cloud/cos-stable-81-12871-119-0"
     size  = 100
   }
 }

 network_interface {
   network = "default"
   network_ip = "10.128.0.2"

   access_config {
     // Include this section to give the VM an external ip address
   }
 }

 metadata_startup_script = <<EOF
docker run -d --restart unless-stopped -p 10.128.0.2:5000:5000 gcr.io/tldr-278619/summary-service -model bert-large-uncased
EOF

 metadata = {
  google-logging-enabled     = "true"
 }

 service_account {
   email = "summarizer@tldr-278619.iam.gserviceaccount.com"
   scopes = [
     "https://www.googleapis.com/auth/cloud-platform"
   ]
 }

 shielded_instance_config {
   enable_integrity_monitoring = true
   enable_secure_boot          = false
   enable_vtpm                 = true
 }
}

# test:
# curl -vvv --data-binary "@./text" -H "Content-type: text/plain" -X POST http://10.128.0.2:5000/summarize?ratio=0.1
