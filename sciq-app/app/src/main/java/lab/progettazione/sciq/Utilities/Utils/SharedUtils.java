package lab.progettazione.sciq.Utilities.Utils;

import android.content.Context;
import android.content.SharedPreferences;

import static android.content.Context.MODE_PRIVATE;

public class SharedUtils {

    /**
     * Utils to retrieve information about user login from Shared Preferences
     *
     * @param context - Context of the current running Activity
     * @return True if user is logged in, false otherwise
     */
    public boolean userLogged(Context context) {
        SharedPreferences isLogged = context.getSharedPreferences("Logged", MODE_PRIVATE);
        return isLogged.getBoolean("isLogged", false);
    }

    /**
     * Utils to retrieve token about user from Shared Preferences
     *
     * @param context
     * @return Token of the user
     */
    public String getToken(Context context) {
        if (userLogged(context)) {
            SharedPreferences pref = context.getSharedPreferences("Info", MODE_PRIVATE);
            String tkn = pref.getString("token", null);
            return tkn;
        } else
            return null;
    }


}
