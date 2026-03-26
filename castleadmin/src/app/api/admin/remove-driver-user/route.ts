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
    const { authUserId, driverId } = await request.json();

    if (!authUserId || !driverId) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
    }

    // First, update the driver record to remove the auth_user_id
    const { error: updateError } = await supabaseAdmin
      .from('drivers')
      .update({ auth_user_id: null })
      .eq('id', driverId);

    if (updateError) {
      console.error('Driver update error:', updateError);
      return NextResponse.json({ error: 'Failed to unlink credentials from driver' }, { status: 500 });
    }

    // Delete the auth user
    const { error: deleteError } = await supabaseAdmin.auth.admin.deleteUser(authUserId);

    if (deleteError) {
      console.error('Auth user deletion error:', deleteError);
      // Still return success since the driver record was updated
      return NextResponse.json({ 
        success: true, 
        warning: 'Credentials unlinked but auth user could not be deleted',
        message: 'Driver credentials removed (partial)' 
      });
    }

    return NextResponse.json({ 
      success: true, 
      message: 'Driver credentials removed successfully' 
    });
  } catch (error: any) {
    console.error('Remove driver user error:', error);
    return NextResponse.json({ error: error.message || 'Internal server error' }, { status: 500 });
  }
}
