# Odoo 16 HIS + AI Diagnosis + WhatsApp — 70-Step Roadmap

---

## Phase 1 — Infrastructure & Initial Odoo Setup
- [ ] Provision DigitalOcean droplet (Ubuntu 22.04 LTS, enable UFW & swap)
- [ ] Create non-root user, configure SSH keys, disable password login, harden SSH
- [ ] Install Docker & Docker Compose (lightweight, for 2GB RAM; add swap if missing)
- [ ] Prepare Postgres container with persistent volume + backup cron
- [ ] Deploy Odoo 16 (community) container, connect to Postgres
- [ ] Create staging DB and test admin user; set timezone to Africa/Mogadishu
- [ ] Configure SMTP for outbound notifications and alerts

---

## Phase 2 — Core HIS Modules & Data Model
- [ ] Install/create modules: EMR/Patient, Appointments, Lab, Pharmacy, HR roster
- [ ] Extend `res.partner`: phone_mobile_e164, whatsapp_opt_in, language, quiet_hours
- [ ] Create encounter model (chief_complaint, vitals, problems)
- [ ] Add lab result model: LOINC code, value, unit, ref_range, status
- [ ] Add prescription hook: meds, dose, frequency, allergies, renal info
- [ ] Load code lists: ICD-10 subset, LOINC, ATC/Rx CSV
- [ ] Role-based access: Clinician, Lab tech, Pharmacist, Admin, Nurse

---

## Phase 3 — WhatsApp Integration
- [ ] Connect Twilio WhatsApp sandbox/number
- [ ] Store WhatsApp opt-in in patient record
- [ ] Basic send message API (appointment reminder, lab result)
- [ ] Inbound message handler → log to encounter
- [ ] Quiet hours filter, language preference

---

## Phase 4 — AI Diagnosis Support
- [ ] Connect OpenAI API (GPT-4/GPT-5)
- [ ] Prompt templates for symptom → differential
- [ ] Add “AI Suggested Diagnosis” field to encounter
- [ ] Add disclaimer + clinician override
- [ ] Track usage metrics

---

## Phase 5 — Lab/Pharmacy Extensions
- [ ] Lab: add specimen type, collection time, verify status
- [ ] Lab: HL7 FHIR import/export skeleton
- [ ] Pharmacy: add inventory, dispensing log, refill reminders
- [ ] Pharmacy: drug-allergy interaction check

---

## Phase 6 — HR & Scheduling
- [ ] Staff roster module
- [ ] Link appointments to clinician schedules
- [ ] Attendance/leave basics
- [ ] Duty roster export to WhatsApp

---

## Phase 7 — Security & Compliance
- [ ] Enable HTTPS (Let’s Encrypt)
- [ ] Enforce role-based access & audit log
- [ ] Backup strategy: DB dumps + file storage
- [ ] Data retention policy

---

## Phase 8 — Testing & Staging
- [ ] Unit test modules (pytest/odoo test framework)
- [ ] Load sample patients, encounters, labs
- [ ] Simulate WhatsApp flows
- [ ] Clinician feedback cycle

---

## Phase 9 — Deployment & Training
- [ ] Deploy production server
- [ ] Train clinicians, lab techs, pharmacists
- [ ] Rollout WhatsApp reminders
- [ ] Monitor logs & errors
- [ ] Incremental rollout by department

---

## Phase 10 — Future Enhancements
- [ ] Voice bot integration (Twilio Voice)
- [ ] Mobile-friendly patient portal
- [ ] AI triage chatbot
- [ ] Analytics dashboards (visits, outcomes, utilization)
- [ ] Multi-language support (Somali, English, Arabic)
