-- =========================================================================
-- Phase 1 DDL Migration: Supabase Row Level Security (RLS) Hardening
-- Finding Reference: SEC-002 (Overly Permissive RLS in Supabase)
-- Specification: MASTER_DEVELOPMENT_SPECIFICATION.md (Section 4.2.3)
-- =========================================================================

-- 1. Ensure Row Level Security (RLS) is explicitly enabled on all core tables
ALTER TABLE IF EXISTS public.services ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.time_slots ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.user_packages ENABLE ROW LEVEL SECURITY;

-- 2. Revoke insecure legacy public write and open read access
DROP POLICY IF EXISTS "Allow public write services" ON public.services;
DROP POLICY IF EXISTS "Allow public write time_slots" ON public.time_slots;
DROP POLICY IF EXISTS "Allow public write bookings" ON public.bookings;
DROP POLICY IF EXISTS "Allow public read bookings" ON public.bookings;
DROP POLICY IF EXISTS "Allow public write user_packages" ON public.user_packages;
DROP POLICY IF EXISTS "Allow public read user_packages" ON public.user_packages;
DROP POLICY IF EXISTS "Enable all access for all users" ON public.services;
DROP POLICY IF EXISTS "Enable all access for all users" ON public.time_slots;
DROP POLICY IF EXISTS "Enable all access for all users" ON public.bookings;
DROP POLICY IF EXISTS "Enable all access for all users" ON public.user_packages;

-- 3. Public catalog browsing: public can read published studio services & time slots
DROP POLICY IF EXISTS "Public read services" ON public.services;
CREATE POLICY "Public read services" ON public.services 
  FOR SELECT TO public 
  USING (true);

DROP POLICY IF EXISTS "Public read time_slots" ON public.time_slots;
CREATE POLICY "Public read time_slots" ON public.time_slots 
  FOR SELECT TO public 
  USING (true);

-- 4. Authenticated clients: can read only their own bookings and wellness packages
DROP POLICY IF EXISTS "Clients read own bookings" ON public.bookings;
CREATE POLICY "Clients read own bookings" ON public.bookings 
  FOR SELECT TO authenticated 
  USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Clients read own packages" ON public.user_packages;
CREATE POLICY "Clients read own packages" ON public.user_packages 
  FOR SELECT TO authenticated 
  USING (auth.uid() = user_id);

-- 5. Backend Service Role: full management reserved strictly for service_role
DROP POLICY IF EXISTS "Service role manages services" ON public.services;
CREATE POLICY "Service role manages services" ON public.services 
  FOR ALL TO service_role 
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Service role manages time_slots" ON public.time_slots;
CREATE POLICY "Service role manages time_slots" ON public.time_slots 
  FOR ALL TO service_role 
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Service role manages bookings" ON public.bookings;
CREATE POLICY "Service role manages bookings" ON public.bookings 
  FOR ALL TO service_role 
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Service role manages user_packages" ON public.user_packages;
CREATE POLICY "Service role manages user_packages" ON public.user_packages 
  FOR ALL TO service_role 
  USING (true)
  WITH CHECK (true);
