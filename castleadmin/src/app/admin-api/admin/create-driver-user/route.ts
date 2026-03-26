import { createClient } from '@supabase/supabase-js';
import { NextRequest, NextResponse } from 'next/server';

// Create admin client with service role key
const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
  { auth: { autoRefreshToken: false, persistSession: false } }
);

export async function POST(request: NextRequest) {
  try {
    const { email, password, driverId, driverName } = await request.json();

    if (!email || !password || !driverId) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
    }

    // Check if email is already in use
    const { data: existingUsers } = await supabaseAdmin.auth.admin.listUsers();
    const emailExists = existingUsers?.users?.some(u => u.email === email);
    if (emailExists) {
      return NextResponse.json({ error: 'Email is already in use by another account' }, { status: 400 });
    }

    // Create the auth user
    const { data: authData, error: authError } = await supabaseAdmin.auth.admin.createUser({
      email,
      password,
      email_confirm: true,
      user_metadata: {
        name: driverName,
        role: 'driver',
        driver_id: driverId,
      },
    });

    if (authError) {
      console.error('Auth user creation error:', authError);
      return NextResponse.json({ error: authError.message }, { status: 400 });
    }

    if (!authData.user) {
      return NextResponse.json({ error: 'Failed to create user' }, { status: 500 });
    }

    // Update the driver record with the auth_user_id
    const { error: updateError } = await supabaseAdmin
      .from('drivers')
      .update({ 
        auth_user_id: authData.user.id,
        email: email,
      })
      .eq('id', driverId);

    if (updateError) {
      // Rollback: delete the auth user if driver update fails
      await supabaseAdmin.auth.admin.deleteUser(authData.user.id);
      console.error('Driver update error:', updateError);
      return NextResponse.json({ error: 'Failed to link credentials to driver' }, { status: 500 });
    }

    return NextResponse.json({ 
      success: true, 
      userId: authData.user.id,
      message: 'Driver credentials created successfully' 
    });
  } catch (error: any) {
    console.error('Create driver user error:', error);
    return NextResponse.json({ error: error.message || 'Internal server error' }, { status: 500 });
  }
}
