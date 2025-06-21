# 🚀 Codingo: Intelligent Tutoring System (ITS)

**Part of Graduation Project – Matrouh University, Faculty of Computers and AI**

**Team Members:**

Hassan Yasser, Ibrahim Mohamed Hassan, Karim Abdulrahim, Omar Abdelaziz, Tarek Saad Fouad, Yasmin Kotb

**Supervisor:** Dr. Fatma Sayed Gadelrab

---

## 🎓 About the Project

**Codingo** is an Intelligent Tutoring System (ITS) designed to offer adaptive, personalized programming education. It dynamically generates custom learning paths based on a learner’s:

* **Programming background**
* **Cognitive learning style** (Felder–Silverman model)
* **Learning goals**

To achieve this, Codingo utilizes:

* **Graph Theory** for curriculum modeling
* **Improved Immune Algorithm (IIA)** for optimal learning path generation
* A **multi-database architecture** (PostgreSQL, MongoDB, Neo4j)

> 📱 The system is built as a cross-platform mobile app using Flutter, with modular microservices for onboarding and learning path generation.

---

## 🧠 Algorithm Repository (This Repo)

This repository contains the **IIA-based recommendation engine**. It processes learner profiles and curriculum graphs to generate optimal Learning Object (LO) sequences personalized to each learner.

### 🧬 How the IIA Algorithm Works

The IIA (Improved Immune Algorithm) is inspired by the human immune system. It evolves a population of candidate paths and selects the best based on **affinity** to the learner's style and **concentration** to avoid redundancy.

#### Key Phases:

1. **Concept Graph Extraction:**

   * Learner goal → Prerequisite subgraph → Topological sort
2. **Antibody Encoding:**

   * Each chromosome represents one LO per concept.
3. **Affinity Calculation:**

   * Each LO has a learning style tag (4D: Active/Reflective, Visual/Verbal, Sensing/Intuitive, Sequential/Global).
   * The algorithm compares LO tags to the learner’s style to calculate affinity scores.
4. **Selection (Pv, SPv):**

   * Chromosomes with better affinity and diversity are selected.
5. **Best Path Output:**

   * Learning path ready for mobile delivery.

### ⚠️ Not Implemented (Deliberately Skipped)

Although **crossover** and **mutation** are common operators in immune-inspired algorithms, they were **intentionally excluded** in our implementation.

🧩 **Why?**
Through testing and analysis, we found that crossover and mutation did **not align with our problem structure**:

* Each chromosome encodes **one LO per concept**, selected based on fixed learning styles.
* Recombining chromosomes risked breaking the semantic and style alignment between LOs and the learner.
* The fitness space was **well-structured** through affinity and concentration without needing artificial diversity.

> 💡 As a result, we focused on **affinity-based selection** (Pv, SPv, and Roulette) to maintain quality and coherence of the paths.

---

## 📱 Related Repositories

* 🔑 [Authentication + Learner Module (Flask)](https://github.com/Tarek-Saad/Graduation-learners-module-backend)
  Manages user registration, FSLSM quiz processing, and profile storage.

* 💡 [Frontend App (Flutter)](https://github.com/HassanYasser07/intelligent_tutoring_system)
  Cross-platform mobile app that presents onboarding, learning paths, LOs, and progress tracking.
