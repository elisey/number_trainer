# GitHub Setup Guide for Number Trainer CI/CD

## 🚀 Quick Setup Checklist

### **1. Repository Configuration**

- [ ] **Repository is public or private** (both work)
- [ ] **GitHub Actions enabled** (Settings → Actions → General)
- [ ] **Packages enabled** (Settings → Packages → General)

### **2. Permissions Setup**

#### **Actions Permissions**
1. Go to **Settings** → **Actions** → **General**
2. Set **Actions permissions** to "Allow all actions and reusable workflows"
3. Set **Workflow permissions** to:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**

#### **Packages Permissions**
1. Go to **Settings** → **Packages**
2. Ensure **Inherit access from source repository** is enabled

### **3. Workflow Files**

Ensure these files exist in your repository:
```
.github/
└── workflows/
    ├── docker-publish.yml      # Production releases
    └── docker-build-test.yml   # Development testing
```

### **4. Test the Setup**

#### **Test Development Workflow**
```bash
# Make a small change and push to main
echo "# Test" >> README.md
git add README.md
git commit -m "Test workflow"
git push origin main
```

**Expected Result**:
- Go to **Actions** tab
- You should see "Build Docker Image (Test Only)" workflow running
- Status should be green ✅

#### **Test Production Workflow**
```bash
# Create a test release
git tag v0.1.0-test
git push origin v0.1.0-test
```

**Expected Result**:
- Go to **Actions** tab
- You should see "Build and Publish Docker Image" workflow running
- Status should be green ✅
- Go to **Packages** tab to see the published image

### **5. Verify Container Registry**

1. Go to **Packages** tab in your repository
2. You should see a package named `number-trainer`
3. Click on it to see available tags

## 🔧 **Troubleshooting**

### **Workflow Not Triggering**
- [ ] Check workflow files are in `.github/workflows/`
- [ ] Verify branch names (main vs master)
- [ ] Check file permissions (should be 644)

### **Permission Errors**
- [ ] Verify Actions permissions in Settings
- [ ] Check Packages permissions
- [ ] Ensure repository is not archived

### **Build Failures**
- [ ] Check workflow logs in Actions tab
- [ ] Verify Dockerfile syntax
- [ ] Check for missing dependencies

## 📊 **Monitoring**

### **Actions Dashboard**
- **URL**: `https://github.com/[username]/number-trainer/actions`
- **Shows**: All workflow runs, status, logs

### **Packages Dashboard**
- **URL**: `https://github.com/[username]/number-trainer/packages`
- **Shows**: Published Docker images and tags

### **Health Check**
```bash
# Test your published image
docker run --rm -p 8000:8000 ghcr.io/[username]/number-trainer:latest
curl http://localhost:8000/api/health
```

## 🎯 **Next Steps**

After setup is complete:

1. **Make your first release**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Deploy to production**:
   ```bash
   docker run -d -p 8000:8000 ghcr.io/[username]/number-trainer:v1.0.0
   ```

3. **Monitor and iterate**:
   - Check Actions for build status
   - Monitor Packages for new releases
   - Use health checks for deployment verification
