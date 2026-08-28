# 🏥 Jarurat Care – Healthcare Support Assistant

A simple full-stack healthcare-support web application developed for the **Jarurat Care Full Stack Developer Internship Assignment**.

The application helps users submit patient support requests, get automated answers to common healthcare-support questions, and allows the support team to manage requests through an admin dashboard.

---

## 🌐 Live Demo

**Live Website:** Add your Render live link here

**GitHub Repository:** Add your GitHub repository link here

---

## 🎯 Project Objective

The goal of this project is to demonstrate how a simple web application can help an NGO organize healthcare-support requests and provide quick answers to common questions.

The application focuses on:

- Simple user experience
- Patient support request collection
- Automated FAQ responses
- Database storage
- Admin-side request management

---

## ✨ Main Features

### 🏠 Home Page

A modern landing page introducing Jarurat Care and providing navigation to the main services.

### 📝 Patient Support

Users can submit a support request with:

- Full Name
- Age
- Phone Number
- Location
- Support Requirement

### 📩 Automatic Confirmation

After successfully submitting the form, the user receives an instant confirmation page.

### 🤖 FAQ Assistant

The automated healthcare-support assistant can answer common questions about:

- Healthcare support
- Doctor appointments
- Emergency guidance
- Medicines
- Symptoms
- Hospitals and clinics
- Patient support requests
- Privacy

### 📊 Admin Dashboard

The dashboard allows the support team to:

- View total requests
- View patient information
- View support requirements
- View submission date and time
- Delete support requests

### 💾 Database

All patient support requests are stored using **SQLite**.

---

## 🧠 AI / Automation Feature

### Healthcare FAQ Assistant

The project includes an automated FAQ assistant that identifies common questions and provides predefined healthcare-support responses.

Example:

**User:**

> How can I make a doctor appointment?

**Jarurat Care Assistant:**

> To make a doctor appointment, contact a nearby hospital or clinic or use the healthcare provider's official appointment system.

This automation can reduce repetitive questions handled manually by an NGO support team.

> Note: The current prototype uses a rule-based automated FAQ system. It provides general information and does not provide medical diagnosis.

---

## 🏥 NGO Use Case

Jarurat Care can be used by an NGO or healthcare-support organization to collect and organize basic support requests from patients.

### Patient workflow

```text
Patient
   ↓
Patient Support Form
   ↓
Request Validation
   ↓
SQLite Database
   ↓
Admin Dashboard
   ↓
Support Team Review