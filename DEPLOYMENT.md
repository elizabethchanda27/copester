# Deployment Guide for Coping Companion

This guide will help you deploy the Coping Companion application to Vercel.

## Prerequisites

- A Vercel account (free at [vercel.com](https://vercel.com))
- Git repository with the project code
- Node.js and Python installed locally for testing

## Deployment Steps

### 1. Backend Deployment (Python Flask API)

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Deploy to Vercel:**

   ```bash
   vercel
   ```

3. **Follow the prompts:**

   - Link to existing project or create new
   - Set project name (e.g., `coping-companion-api`)
   - Deploy

4. **Note the deployment URL** (e.g., `https://coping-companion-api.vercel.app`)

### 2. Frontend Deployment (React App)

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

2. **Set the backend API URL:**
   Create a `.env` file in the frontend directory:

   ```bash
   echo "REACT_APP_API_URL=https://your-backend-url.vercel.app/api" > .env
   ```

   Replace `your-backend-url` with your actual backend URL.

3. **Deploy to Vercel:**

   ```bash
   vercel
   ```

4. **Follow the prompts:**
   - Link to existing project or create new
   - Set project name (e.g., `coping-companion-frontend`)
   - Deploy

### 3. Environment Variables

For the backend, you may need to set environment variables in Vercel:

1. Go to your Vercel dashboard
2. Select your backend project
3. Go to Settings > Environment Variables
4. Add any necessary environment variables

### 4. Database Considerations

**Important:** The current setup uses SQLite, which is file-based and won't persist between serverless function calls on Vercel. For production, consider:

1. **Using a cloud database** (PostgreSQL on Vercel, Supabase, etc.)
2. **Updating the backend code** to use the cloud database
3. **Setting up database connection strings** as environment variables

### 5. Custom Domain (Optional)

1. In your Vercel dashboard, go to your project
2. Navigate to Settings > Domains
3. Add your custom domain
4. Configure DNS settings as instructed

## Local Development

### Running Locally

1. **Start the backend:**

   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Start the frontend:**

   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Testing the API

You can test the API endpoints using curl or a tool like Postman:

```bash
# Health check
curl https://your-backend-url.vercel.app/api/health

# Get journal entries
curl https://your-backend-url.vercel.app/api/entries

# Create a journal entry
curl -X POST https://your-backend-url.vercel.app/api/entries \
  -H "Content-Type: application/json" \
  -d '{"date":"2024-01-15","mood_rating":7,"content":"Feeling good today!"}'
```

## Troubleshooting

### Common Issues

1. **CORS Errors:**

   - Ensure the backend has CORS properly configured
   - Check that the frontend is using the correct API URL

2. **Database Issues:**

   - SQLite won't work in production on Vercel
   - Consider migrating to a cloud database

3. **Build Errors:**

   - Check that all dependencies are properly listed in package.json
   - Ensure Python requirements.txt is up to date

4. **API Connection Issues:**
   - Verify the REACT_APP_API_URL environment variable is set correctly
   - Check that the backend is deployed and accessible

### Getting Help

- Check Vercel deployment logs in the dashboard
- Review the application logs for errors
- Test API endpoints individually
- Verify environment variables are set correctly

## Security Considerations

1. **Environment Variables:** Never commit sensitive data to your repository
2. **API Keys:** Store API keys and secrets in Vercel environment variables
3. **CORS:** Configure CORS properly for production domains
4. **HTTPS:** Vercel provides HTTPS by default

## Performance Optimization

1. **Image Optimization:** Vercel automatically optimizes images
2. **Caching:** Configure appropriate cache headers
3. **CDN:** Vercel provides global CDN by default
4. **Database:** Use connection pooling for database connections

## Monitoring

1. **Vercel Analytics:** Enable analytics in your Vercel dashboard
2. **Error Tracking:** Consider adding error tracking (Sentry, etc.)
3. **Performance Monitoring:** Monitor API response times and frontend performance

## Updates and Maintenance

1. **Automatic Deployments:** Vercel automatically deploys on git pushes
2. **Rollbacks:** You can rollback to previous deployments in the Vercel dashboard
3. **Environment Management:** Use different environments for staging and production
