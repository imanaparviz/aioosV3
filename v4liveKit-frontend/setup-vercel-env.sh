#!/bin/bash
# Setup Vercel Environment Variables

echo "Setting up Vercel environment variables..."

vercel env add VITE_SUPABASE_URL production <<EOF
https://tctfeentpoafteuphpls.supabase.co
EOF

vercel env add VITE_SUPABASE_ANON_KEY production <<EOF
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRjdGZlZW50cG9hZnRldXBocGxzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE4Nzc3NzMsImV4cCI6MjA3NzQ1Mzc3M30.MoQToMiEfGsdPYMfa0V59odq_i3QRrEyD8P2dmQu4Pg
EOF

echo "✅ Environment variables added!"
echo "Now deploying to production..."

vercel --prod

echo "🎉 Deployment complete!"

