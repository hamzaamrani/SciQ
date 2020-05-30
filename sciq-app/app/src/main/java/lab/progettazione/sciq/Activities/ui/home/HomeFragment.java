package lab.progettazione.sciq.Activities.ui.home;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.google.android.material.textfield.TextInputEditText;
import com.hbisoft.pickit.PickiT;
import com.hbisoft.pickit.PickiTCallbacks;
import com.nishant.math.MathView;
import com.progettazione.sciq.R;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.ArrayList;

import lab.progettazione.sciq.Activities.Login.SignupActivity;
import lab.progettazione.sciq.Activities.ui.ShowResults;
import lab.progettazione.sciq.Model.Expression;
import lab.progettazione.sciq.Utilities.AsyncTasks.SendImage;
import lab.progettazione.sciq.Utilities.AsyncTasks.SubmitExpression;
import lab.progettazione.sciq.Utilities.Interfaces.ExpressionInterface;
import lab.progettazione.sciq.Utilities.Interfaces.ReturnString;
import lab.progettazione.sciq.Utilities.Utils.SharedUtils;

import static java.lang.String.valueOf;


public class HomeFragment extends Fragment implements ExpressionInterface, PickiTCallbacks, ReturnString {

    private static final int CAMERA_REQUEST = 100;
    private static final int PICK_FROM_GALLERY = 42;
    private PickiT pickiT;
    private HomeViewModel homeViewModel;
    private SubmitExpression submitExpression;
    private SharedUtils check = new SharedUtils();
    private static String asciiMath_delimiter = "`";

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        homeViewModel = ViewModelProviders.of(this).get(HomeViewModel.class);
        View root = inflater.inflate(R.layout.fragment_home, container, false);
        final TextView textView = root.findViewById(R.id.text_home);
        final LinearLayout preview = root.findViewById(R.id.preview);
        final TextInputEditText expression_input = root.findViewById(R.id.expression_input);
        final MathView mathView = root.findViewById(R.id.math_view);
        final Button submit_expression = root.findViewById(R.id.submit_expression);
        final ProgressBar progressBar = root.findViewById(R.id.my_progressBar);
        final ImageButton send_photo = root.findViewById(R.id.send_photo);
        final ImageButton attach_photo = root.findViewById(R.id.attach_photo);

        pickiT = new PickiT(getContext(), this);


        expression_input.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                preview.setVisibility(View.VISIBLE);
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                mathView.setText(asciiMath_delimiter + s.toString() + asciiMath_delimiter);
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        submit_expression.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                submitExpression = new SubmitExpression(getContext(), progressBar);
                submitExpression.setDelegate(HomeFragment.this);
                if (expression_input.getText().length() > 0) {
                    expression_input.setError(null);
                    if (check.userLogged(getContext())) {
                        submitExpression.execute(check.getToken(getContext()), expression_input.getText().toString().trim());
                    } else {
                        submitExpression.execute(null, expression_input.getText().toString().trim());
                    }
                } else
                    expression_input.setError("Type some kind of expression to be evaluated!");
            }
        });


        homeViewModel.getText().observe(getViewLifecycleOwner(), new Observer<String>() {
            @Override
            public void onChanged(@Nullable String s) {
                textView.setText(s);
            }
        });


        send_photo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //TODO Camera intent
                /* Create an intent to handle photo */
                Intent intentCamera = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(intentCamera, CAMERA_REQUEST);
            }
        });

        attach_photo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openFolder();
            }
        });


        return root;
    }


    @Override
    public void onExpressionSuccessful(Expression expression) {
        Log.d("submit_expression", "Request successful");
        System.out.println(expression.toString());
        Intent i = new Intent(getContext(), ShowResults.class);
        i.putExtra("Expression", expression);
        startActivity(i);
    }

    @Override
    public void onExpressionFailure(String error) {
        if (error.equalsIgnoreCase("Limit request reached!")) {
            new AlertDialog.Builder(getContext())
                    .setTitle("Limit request reached!")
                    .setMessage("Sign up or login to perform unlimited requests!")
                    .setPositiveButton("Ok, let's do it", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Intent i = new Intent(getContext(), SignupActivity.class);
                            i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                            startActivity(i);
                            getActivity().finish();
                        }
                    })
                    .setNegativeButton("No thanks", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            // Do nothing
                        }
                    }).show();
        }
    }

    public void openFolder() {
        String[] mimeTypes =
                {"application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", // .doc & .docx"application/vnd.ms-powerpoint","application/vnd.openxmlformats-officedocument.presentationml.presentation", // .ppt & .pptx
                        "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", // .xls & .xlsx
                        "text/plain",
                        "application/pdf",
                        "application/zip",
                        "image/*"};
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("*/*");
        intent.putExtra(Intent.EXTRA_MIME_TYPES, mimeTypes);
        startActivityForResult(intent, PICK_FROM_GALLERY);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == Activity.RESULT_OK) {
            switch (requestCode) {
                case 100:
                    Uri tempUri = null;
                    try {
                        Bitmap bp = (Bitmap) data.getExtras().get("data");
                        tempUri = getImageUri(getContext(), bp);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    if (tempUri != null) {
                        //case_camera = true;
                        pickiT.getPath(tempUri, Build.VERSION.SDK_INT);
                    }
                    break;
                case PICK_FROM_GALLERY:
                    InputStream is = null;
                    String path = null;
                    Uri uri;
                    String filename;
                    int i;
                    String current_path;
                    if (null != data) { // checking empty selection
                        if (null != data.getClipData()) { // checking multiple selection or not
                            for (i = 0; i < data.getClipData().getItemCount(); i++) {
                                uri = data.getClipData().getItemAt(i).getUri();
                                pickiT.getPath(uri, Build.VERSION.SDK_INT);
                            }
                        } else { // single selection
                            uri = data.getData();
                            //System.out.println(uri);
                            if (uri != null) {
                                pickiT.getPath(uri, Build.VERSION.SDK_INT);
                            }
                        }
                    } else
                        Toast.makeText(getContext(), "Something went wrong getting file!", Toast.LENGTH_LONG).show();
                    break;
            }
        }
    }

    public Uri getImageUri(Context inContext, Bitmap inImage) {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        inImage.compress(Bitmap.CompressFormat.JPEG, 100, bytes);
        String path = MediaStore.Images.Media.insertImage(inContext.getContentResolver(), inImage, "Title", null);
        System.out.println(path);
        return Uri.parse(path);
    }

    @Override
    public void PickiTonStartListener() {

    }

    @Override
    public void PickiTonProgressUpdate(int progress) {

    }

    @Override
    public void PickiTonCompleteListener(String path, boolean wasDriveFile, boolean wasUnknownProvider, boolean wasSuccessful, String Reason) {
        //Attachments attach;
        Log.d("PickIT", valueOf(wasSuccessful));
        ArrayList<String> paths = new ArrayList<>();


        paths.add(check.getToken(getContext()));
        paths.add(path);

        SendImage sendImage = new SendImage(getContext());
        sendImage.setDelegate(HomeFragment.this);
        sendImage.execute(paths);
    }

    @Override
    public void processFinish(String output) {
        Boolean success;
        try {
            JSONObject response = new JSONObject(output);
            if (response.has("success")) {
                success = response.getBoolean("success");
                if (success) {
                    Expression response_exp = new Expression(response);
                    System.out.println("Success =  " + response_exp.getSuccess());
                    Intent i = new Intent(getContext(), ShowResults.class);
                    i.putExtra("Expression", response_exp);
                    startActivity(i);
                } else
                    Toast.makeText(getContext(), "OPS, I didn't found an expression, please retry!", Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getContext(), "Connection error", Toast.LENGTH_LONG).show();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
