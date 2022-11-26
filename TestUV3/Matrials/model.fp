varying highp vec4 var_position;
varying mediump vec3 var_normal;
varying mediump vec2 var_texcoord0;
varying mediump vec4 var_light;

uniform lowp sampler2D tex0;
uniform lowp vec4 tint;
const vec2 vp = vec2(8000.0);
const float pi = 3.1415926435;
vec2 iResolution = vec2(960,640) ; 
float iTime = tint.x *0.1; 
vec2 iMouse = vec2(1.0) ; 


void main()
{
    vec2 fragCoord =  var_texcoord0.xy *vec2(iResolution.x/iResolution.y,1.0) -0.5; 
    float t = iTime * 10.0 + iMouse.x;
    vec2 uv = fragCoord ;
    vec2 p0 = (uv - 0.5) * vp;
    vec2 hvp = vp * 0.5;
    vec2 p1d = vec2(cos( t / 98.0),  sin( t / 178.0)) * hvp - p0;
    vec2 p2d = vec2(sin(-t / 124.0), cos(-t / 104.0)) * hvp - p0;
    vec2 p3d = vec2(cos(-t / 165.0), cos( t / 45.0))  * hvp - p0;
    float sum = 1.0 + 0.5 * (
        cos(length(p1d) / 10.0) +
        cos(length(p2d) / 20.0) +
        sin(length(p3d) / 20.0) * sin(p3d.x / 20.0) * sin(p3d.y / 15.0));

        float i = fragCoord.x;
        vec3 ti = (iTime + iMouse.y) / vec3(63.0, 78.0, 45.0);
        vec3 csi = cos(i * pi * 2.0 + vec3(0.0, 1.0, -0.5) * pi + ti);
        vec3 colorx = normalize(vec3(vec3( 255, 87, 51 )));


        //---
        vec2 p = fragCoord.xy ; 
        vec3 colorup = vec3(6,66,115) ; 
        vec3 colordown =  vec3(43, 101, 236) ; 
        colordown = normalize(colordown) ;
        colorup = normalize(colorup) ; 
        vec3 mixed = mix(texture2D(tex0, var_texcoord0.xy).xyz,colordown,.5*fract(sum)) ; 
        gl_FragColor = vec4(mixed,1.0); 
        //gl_FragColor = vec4(fract(sum)*8*colordown, 1);
        //gl_FragColor = texture2D(tex0, var_texcoord0.xy) ; 
    }
    


/*

varying highp vec4 var_position;
varying mediump vec3 var_normal;
varying mediump vec2 var_texcoord0;
varying mediump vec4 var_light;

uniform lowp sampler2D tex0;
uniform lowp vec4 tint;

void main()
{
    // Pre-multiply alpha since all runtime textures already are
    vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);
    vec4 color = texture2D(tex0, var_texcoord0.xy) * tint_pm;

    // Diffuse light calculations
    vec3 ambient_light = vec3(0.2);
    vec3 diff_light = vec3(normalize(var_light.xyz - var_position.xyz));
    diff_light = max(dot(var_normal,diff_light), 0.0) + ambient_light;
    diff_light = clamp(diff_light, 0.0, 1.0);

    gl_FragColor = vec4(color.rgb*diff_light,1.0);
}
*/




