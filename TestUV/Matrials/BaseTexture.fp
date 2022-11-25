varying highp vec4 var_position;
varying mediump vec3 var_normal;
varying mediump vec2 fragCoord;
varying highp vec4 var_color0;
varying mediump vec4 var_light;

uniform lowp sampler2D tex0;
vec2 iResolution = vec2(960,640) ; 


void main()
{
    float sunR = 0.006 ; 
    vec3 sunColor = vec3(1.0,1.0,0.8) ; 
    vec2 sunpos = vec2(0.15 ) ; 
        sunpos  = sunpos *vec2(iResolution.x/iResolution.y,1.0) ; 
        vec2 p = fragCoord.xy ;
        vec2 uv = fragCoord.xy *vec2(iResolution.x/iResolution.y,1.0) -0.5; 
        vec3 colorup = vec3(9,108,167) ; 
        vec3 colordown = vec3(250,242,239) ; 
        colordown = normalize(colordown) ;
        colorup = normalize(colorup) ; 
        vec3 mixed = mix(colordown,colorup,p.y) ; 
        vec4 fragColor = vec4(mixed,1.0); 
        float distance_cubic = (uv.x - sunpos.x)*(uv.x - sunpos.x) + (uv.y - sunpos.y)*(uv.y - sunpos.y) ; 
        if (distance_cubic < sunR*sunR ){

            fragColor = vec4(sunColor,1.0) ; 
        }
        else{

            fragColor = vec4(mix(mixed , sunColor, (sunR*sunR)/distance_cubic),1) ; 
        }

    gl_FragColor = fragColor ; 
}

