# Odoo 16 HIS + AI Diagnosis + WhatsApp — Roadmap

## Phase 1 — Infrastructure & Initial Odoo Setup
- [ ] Provision DigitalOcean droplet (Ubuntu 22.04 LTS, enable UFW & swap)
- [ ] Create non-root user, configure SSH keys, harden SSH
- [ ] Install Docker & Docker Compose (lightweight for 2GB RAM)
- [ ] Prepare Postgres container with persistent volume + backup cron
- [ ] Deploy Odoo 16 (community) container, connect to Postgres
- [ ] Create staging DB, test admin user, set timezone Africa/Mogadishu
- [ ] Configure SMTP for outbound notifications

## Phase 2 — Core HIS Modules & Data Model
- [ ] Install or create modules: EMR/Patient, Appointments, Lab, Pharmacy, HR roster
- [ ] Extend `res.partner` with phone_mobile_e164, whatsapp_opt_in, language, quiet_hours
- [ ] Create encounter model (chief_complaint, vitals, problems)
- [ ] Add lab result model (LOINC code, value, unit, ref_range, status)
- [ ] Add prescription hook (meds, dose, frequency, allergies, renal info)
- [ ] Load code lists: ICD-10 subset, LOINC common tests, ATC/Rx CSV
- [ ] Configure RBAC: Clinician, Lab tech, Pharmacist, Admin, Nurse
